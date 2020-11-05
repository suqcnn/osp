package kube_resource

import (
	"github.com/openspacee/osp/pkg/utils"
)

const (
	ListAction     = "list"
	ExecAction     = "exec"
	GetAction      = "get"
	StdinAction    = "stdin"
	OpenLogAction  = "openLog"
	CloseLogAction = "closeLog"
)

type KubeResource struct {
	ResType     string
	KubeMessage *MiddleMessage
}

func (k *KubeResource) Get(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, GetAction, params)
}

func (k *KubeResource) List(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, ListAction, params)
}

func (k *KubeResource) Exec(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, ExecAction, params)
}

func (k *KubeResource) Stdin(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, StdinAction, params)
}

func (k *KubeResource) OpenLog(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, OpenLogAction, params)
}

func (k *KubeResource) CloseLog(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, CloseLogAction, params)
}

func (k *KubeResource) request(cluster, action string, params interface{}) *utils.Response {
	middleRequest := NewMiddleRequest(cluster, k.ResType, action, params, 10)
	res := k.KubeMessage.SendRequest(middleRequest)
	return res
}

const (
	PodType = "pod"
)

type KubeResources struct {
	Pod *KubeResource
}

func NewKubeResources(message *MiddleMessage) *KubeResources {
	return &KubeResources{
		Pod: &KubeResource{ResType: PodType, KubeMessage: message},
	}
}
