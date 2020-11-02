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
	wsReceiveChan chan []byte
	wsCloseChan   chan struct{}
}

func NewKubeWebsocket(cluster string, ws *websocket.Conn, redisOp *redis.Options) *KubeWebsocket {
	middleMsg := kube_resource.NewMiddleMessage(redisOp)
	return &KubeWebsocket{
		cluster:       cluster,
		redisOptions:  redisOp,
		middleMessage: middleMsg,
		wsConn:        ws,
		wsReceiveChan: make(chan []byte),
		wsCloseChan:   make(chan struct{}),
	}
}

func (k *KubeWebsocket) Consume() {
	klog.Info("start consume cluster ", k.cluster)
	go k.WsReceiveMsg()
	go k.MiddleRequestHandle()

	go func() {
		for {
			select {
			case data := <-k.wsReceiveChan:
				klog.Info(string(data))
				midResp, err := kube_resource.UnserialzerMiddleResponse(string(data))
				if err != nil {
					klog.Errorf("unserializer data error: %s", err.Error())
					continue
				}
				k.middleMessage.SendResponse(midResp)
			case <-k.wsCloseChan:
				klog.Info("websocket closed")
				break
			}
		}
	}()
}

func (k *KubeWebsocket) MiddleRequestHandle() {
	middleReqChan := make(chan *kube_resource.MiddleRequest)
	go k.middleMessage.ReceiveRequest(k.cluster, middleReqChan)
	for {
		select {
		case midReq := <-middleReqChan:
			klog.Info(midReq)
			//midResponse := kube_resource.NewMiddleResponse(midReq.RequestId, "request", "test")
			//k.middleMessage.SendResponse(midResponse)
			serReq, _ := midReq.Serializer()
			k.wsConn.WriteMessage(websocket.TextMessage, serReq)
		}
	}
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
		k.wsReceiveChan <- data
	}
}

func (k *KubeWebsocket) Clean() {
	klog.Infof("start clean cluster %s websocket", k.cluster)
	k.wsConn.Close()
	k.middleMessage.Close()
	k.wsCloseChan <- struct{}{}
}
