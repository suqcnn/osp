package kube_resource

import (
	"context"
	"github.com/go-redis/redis/v8"
	oredis "github.com/openspacee/osp/pkg/redis"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
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

func (m *MiddleMessage) ClusterRequestQueueKey(cluster string) string {
	return "osp:cluster_request:" + cluster
}

func (m *MiddleMessage) SendRequest(request *MiddleRequest) *utils.Response {
	r := m.client.HGetAll(m.Context, "osp:cluster:"+request.Cluster)
	return &utils.Response{Code: code.Success, Data: r.Val()}
}
