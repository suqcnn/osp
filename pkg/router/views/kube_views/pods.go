package kube_views

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/ospagent/pkg/utils/code"
	"net/http"
)

type Pod struct {
	Views       []*views.View
	PodResource *kube_resource.KubeResource
}

func NewPod(middleMessage *kube_resource.MiddleMessage) *Pod {
	pod := &Pod{
		PodResource: kube_resource.NewKubeResource(kube_resource.PodType, middleMessage),
	}
	vs := []*views.View{
		views.NewView(http.MethodGet, "/:cluster/list", pod.list),
	}
	pod.Views = vs
	return pod
}

func (p *Pod) list(c *views.Context) *utils.Response {
	var ser ListSerializers
	if err := c.ShouldBind(ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":           ser.Name,
		"namespace":      ser.Namespace,
		"label_selector": ser.LabelSelector,
	}
	return p.PodResource.List(c.Param("cluster"), reqParams)
}
