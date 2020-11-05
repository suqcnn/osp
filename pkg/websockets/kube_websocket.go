package websockets

import (
	"github.com/gorilla/websocket"
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/redis"
	"k8s.io/klog"
)

type KubeWebsocket struct {
	redisOptions  *redis.Options
	middleMessage *kube_resource.MiddleMessage
	cluster       string
	wsConn        *websocket.Conn
	stopped       bool
}

func NewKubeWebsocket(cluster string, ws *websocket.Conn, redisOp *redis.Options) *KubeWebsocket {
	middleMsg := kube_resource.NewMiddleMessage(redisOp)
	return &KubeWebsocket{
		cluster:       cluster,
		redisOptions:  redisOp,
		middleMessage: middleMsg,
		wsConn:        ws,
		stopped:       false,
	}
}

func (k *KubeWebsocket) Consume() {
	klog.Info("start consume cluster ", k.cluster)
	go k.WsReceiveMsg()
	go k.MiddleRequestHandle()
}

func (k *KubeWebsocket) MiddleRequestHandle() {
	for !k.stopped {
		klog.Info("start receive request from cluster ", k.cluster)
		k.middleMessage.ReceiveRequest(k.cluster, func(mr *kube_resource.MiddleRequest) {
			serReq, _ := mr.Serializer()
			k.wsConn.WriteMessage(websocket.TextMessage, serReq)
		})
	}
	klog.Info("middle request handle end")
}

func (k *KubeWebsocket) WsReceiveMsg() {
	defer k.Clean()
	for {
		_, data, err := k.wsConn.ReadMessage()
		if err != nil {
			klog.Error("read err:", err)
			break
		}
		klog.Infof("read data: %s", string(data))
		midResp, err := kube_resource.UnserialzerMiddleResponse(string(data))
		if err != nil {
			klog.Errorf("unserializer data error: %s", err.Error())
			continue
		}
		if midResp.IsRequest() {
			k.middleMessage.SendResponse(midResp)
		} else if midResp.IsTerm() {
			k.middleMessage.SendTerm(midResp)
		} else if midResp.IsWatch() {
			k.middleMessage.SendWatch(k.cluster, midResp)
		} else if midResp.IsLog() {
			k.middleMessage.SendLog(midResp)
		}
	}
}

func (k *KubeWebsocket) Clean() {
	klog.Infof("start clean cluster %s websocket", k.cluster)
	k.middleMessage.Close()
	k.stopped = true
	k.wsConn.Close()
	klog.Info("end clean cluster websocket")
}
