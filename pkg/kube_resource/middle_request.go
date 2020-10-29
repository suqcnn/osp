package kube_resource

import "github.com/openspacee/osp/pkg/utils"

type MiddleRequest struct {
	Cluster   string
	RequestId string
	Resource  string
	Action    string
	Params    interface{}
	Timeout   int
}

func NewMiddleRequest(cluster, requestId, resType, action string, params interface{}, timeout int) *MiddleRequest {
	if requestId == "" {
		requestId = utils.CreateUUID()
	}
	if timeout <= 0 {
		timeout = 30
	}
	return &MiddleRequest{
		Cluster:   cluster,
		RequestId: requestId,
		Resource:  resType,
		Action:    action,
		Params:    params,
		Timeout:   timeout,
	}
}
