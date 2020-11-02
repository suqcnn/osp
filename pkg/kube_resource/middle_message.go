package kube_resource

import (
	"context"
	"encoding/json"
	"github.com/go-redis/redis/v8"
	oredis "github.com/openspacee/osp/pkg/redis"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"k8s.io/klog"
	"time"
)

type MiddleMessage struct {
	options *oredis.Options
	client  *redis.Client
	context.Context
}

func NewMiddleMessage(op *oredis.Options) *MiddleMessage {
	client := oredis.NewRedisClient(op)
	var ctx = context.Background()

	return &MiddleMessage{
		options: op,
		client:  client,
		Context: ctx,
	}
}

func (m *MiddleMessage) Close() {
	m.client.Close()
}

func (m *MiddleMessage) ClusterRequestQueueKey(cluster string) string {
	return "osp:cluster_request:" + cluster
}

func (m *MiddleMessage) ReceiveRequest(cluster string, reqChan chan *MiddleRequest) error {
	reqSubKey := m.ClusterRequestQueueKey(cluster)
	pubsub := m.client.Subscribe(m.Context, reqSubKey)
	defer pubsub.Close()
	klog.Infof("start receive pubsub %s message", cluster)
	for {
		data, err := pubsub.ReceiveMessage(m.Context)
		if err != nil {
			klog.Errorf("receive message error: %s", err.Error())
			return err
		}
		klog.Info(data.Payload)
		mr, err := UnserializerMiddleRequest(data.Payload)
		if err != nil {
			klog.Errorf("unserialzier request error: %s", err.Error())
			continue
		}
		reqChan <- mr
	}
}

func (m *MiddleMessage) SendRequest(request *MiddleRequest) *utils.Response {
	reqPubKey := m.ClusterRequestQueueKey(request.Cluster)
	subNums, err := m.client.PubSubNumSub(m.Context, reqPubKey).Result()
	if err != nil {
		return &utils.Response{Code: code.RedisError, Msg: err.Error()}
	}
	if num, ok := subNums[reqPubKey]; !ok || num <= 0 {
		klog.Infof("cluster %s is not in subscribe", request.Cluster)
		return &utils.Response{Code: code.RequestError, Msg: "connect kubernetes agent error"}
	}
	reqData, err := request.Serializer()
	if err != nil {
		klog.Errorf("middle request error: %s", err.Error())
		return &utils.Response{Code: code.RequestError, Msg: err.Error()}
	}
	_, err = m.client.Publish(m.Context, reqPubKey, reqData).Result()
	if err != nil {
		klog.Error("publish request error: %s", err.Error())
		return &utils.Response{Code: code.RedisError, Msg: err.Error()}
	}

	resData, err := m.client.BLPop(m.Context, time.Duration(request.Timeout)*time.Second, request.RequestId).Result()
	klog.Info(resData)
	if len(resData) < 2 {
		klog.Errorf("get cluster %s response empty", request.Cluster)
		return &utils.Response{Code: code.RequestError, Msg: "request kubernetes agent timeout"}
	}
	if err != nil {
		klog.Errorf("get response error: %s", err.Error())
		return &utils.Response{Code: code.RedisError, Msg: err.Error()}
	}
	var resp utils.Response
	json.Unmarshal([]byte(resData[1]), &resp)

	return &resp
}

func (m *MiddleMessage) SendResponse(midRes *MiddleResponse) {
	reqId := midRes.RequestId
	serData, _ := midRes.Serializer()
	m.client.LPush(m.Context, reqId, serData)
	m.client.Expire(m.Context, reqId, time.Second*3)
	//pipeLine := m.client.Pipeline()
	//pipeLine.LPush(m.Context, reqId, midRes.Serializer())

}
