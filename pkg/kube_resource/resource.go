package kube_resource

import (
	"github.com/openspacee/osp/pkg/utils"
)

const (
	ListAction = "list"
)

type KubeResource struct {
	ResType     string
	KubeMessage *MiddleMessage
}

func (k *KubeResource) List(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, ListAction, params)
}

func (k *KubeResource) request(cluster, action string, params interface{}) *utils.Response {
	middleRequest := NewMiddleRequest(cluster, "", k.ResType, action, params, 30)
	res := k.KubeMessage.SendRequest(middleRequest)
	return res
}

const (
	PodType = "Pod"
)

func NewKubeResource(resType string, message *MiddleMessage) *KubeResource {
	return &KubeResource{
		ResType:     resType,
		KubeMessage: message,
	}
}
