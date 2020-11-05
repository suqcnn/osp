package kube_resource

import (
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
)

const (
	ListAction       = "list"
	ExecAction       = "exec"
	GetAction        = "get"
	DeleteAction     = "delete"
	UpdateYamlAction = "update_yaml"
	UpdateObjAction  = "update_obj"
	StdinAction      = "stdin"
	OpenLogAction    = "openLog"
	CloseLogAction   = "closeLog"
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

func (k *KubeResource) Delete(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, DeleteAction, params)
}

func (k *KubeResource) UpdateYaml(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, UpdateYamlAction, params)
}

func (k *KubeResource) UpdateObj(cluster string, params interface{}) *utils.Response {
	return k.request(cluster, UpdateObjAction, params)
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

type WatchResource struct {
	*KubeResource
}

func (w *WatchResource) OpenWatch(cluster string) *utils.Response {
	return w.Get(cluster, map[string]interface{}{"action": "open"})
}

func (w *WatchResource) CloseWatch(cluster string) *utils.Response {
	hasReceive := w.KubeMessage.HasWatchReceive(cluster)
	if !hasReceive {
		return w.Get(cluster, map[string]interface{}{"action": "close"})
	}
	return &utils.Response{Code: code.Success}
}

const (
	WatchResType    = "watch"
	PodType         = "pod"
	ClusterType     = "cluster"
	EventType       = "event"
	NodeType        = "node"
	DeploymentType  = "deployment"
	StatefulsetType = "statefulset"
	DaemonsetType   = "daemonset"
	CronjobType     = "cronjob"
	JobType         = "job"
	NamespaceType   = "namespace"
)

type KubeResources struct {
	Watch       *WatchResource
	Pod         *KubeResource
	Cluster     *KubeResource
	Event       *KubeResource
	Node        *KubeResource
	Deployment  *KubeResource
	Statefulset *KubeResource
	Daemonset   *KubeResource
	Cronjob     *KubeResource
	Job         *KubeResource
	Namespace   *KubeResource
}

func NewKubeResources(message *MiddleMessage) *KubeResources {
	return &KubeResources{
		Watch:       &WatchResource{&KubeResource{ResType: WatchResType, KubeMessage: message}},
		Pod:         &KubeResource{ResType: PodType, KubeMessage: message},
		Cluster:     &KubeResource{ResType: ClusterType, KubeMessage: message},
		Event:       &KubeResource{ResType: EventType, KubeMessage: message},
		Node:        &KubeResource{ResType: NodeType, KubeMessage: message},
		Deployment:  &KubeResource{ResType: DeploymentType, KubeMessage: message},
		Statefulset: &KubeResource{ResType: StatefulsetType, KubeMessage: message},
		Daemonset:   &KubeResource{ResType: DaemonsetType, KubeMessage: message},
		Cronjob:     &KubeResource{ResType: CronjobType, KubeMessage: message},
		Job:         &KubeResource{ResType: JobType, KubeMessage: message},
		Namespace:   &KubeResource{ResType: NamespaceType, KubeMessage: message},
	}
}
