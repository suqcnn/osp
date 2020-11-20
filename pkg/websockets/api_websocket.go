package websockets

import (
	"encoding/json"
	"github.com/gorilla/websocket"
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/redis"
	"k8s.io/klog"
)

type ApiWebsocket struct {
	redisOptions *redis.Options
	wsConn       *websocket.Conn
	*kube_resource.KubeResources
}

func NewApiWebsocket(ws *websocket.Conn, redisOp *redis.Options, kr *kube_resource.KubeResources) *ApiWebsocket {
	return &ApiWebsocket{
		redisOptions:  redisOp,
		wsConn:        ws,
		KubeResources: kr,
	}
}

func (a *ApiWebsocket) Consume() {
	klog.Info("start consume api ")
	go a.WsReceiveMsg()
}

func (a *ApiWebsocket) WsReceiveMsg() {
	defer a.wsConn.Close()
	middleMessage := kube_resource.NewMiddleMessage(a.redisOptions)
	stopWatch := false
	startWatch := false
	stopChan := make(chan struct{})
	defer func() {
		stopWatch = true
		middleMessage.Close()
		if startWatch {
			<-stopChan
		}
		klog.Info("end receive watch")
	}()
	klog.Info("start read message")
	for {
		_, data, err := a.wsConn.ReadMessage()
		if err != nil {
			klog.Error("read err:", err)
			break
		}
		klog.Infof("read data: %s", string(data))
		var apiMsg ApiMsg
		err = json.Unmarshal(data, &apiMsg)
		if err != nil {
			klog.Error("json error")
			continue
		}
		if apiMsg.Action == "watchCluster" {
			stopWatch = true
			if startWatch {
				middleMessage.Close()
				<-stopChan
				middleMessage = kube_resource.NewMiddleMessage(a.redisOptions)
			}
			clusterMsg := apiMsg.Params.(map[string]interface{})
			cluster := clusterMsg["cluster"].(string)
			klog.Info(cluster)
			if cluster != "" {
				startWatch = true
				go func() {
					stopWatch = false
					resp := a.Watch.OpenWatch(cluster)
					if !resp.IsSuccess() {
						startWatch = false
						klog.Errorf("open watch error: %s", resp.Msg)
						return
					}
					for !stopWatch {
						klog.Info("start receive watch data")
						middleMessage.ReceiveWatch(cluster, func(data string) {
							a.wsConn.WriteMessage(websocket.TextMessage, []byte(data))
						})
					}
					a.Watch.CloseWatch(cluster)
					klog.Info("end receive")
					stopChan <- struct{}{}
					klog.Info("end receive watch data")
				}()
			} else {
				startWatch = false
			}
		}
	}
	klog.Info("end receive api websocket")
}

type ApiMsg struct {
	Action string      `json:"action"`
	Params interface{} `json:"params"`
}
