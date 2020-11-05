package kube_views

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/ospagent/pkg/utils/code"
	"net/http"
)

type Pod struct {
	Views []*views.View
	*kube_resource.KubeResources
}

func NewPod(kr *kube_resource.KubeResources) *Pod {
	pod := &Pod{
		KubeResources: kr,
	}
	vs := []*views.View{
		views.NewView(http.MethodPost, "/:cluster/list", pod.list),
		views.NewView(http.MethodGet, "/:cluster/:namespace/:name", pod.get),
	}
	pod.Views = vs
	return pod
}

func (p *Pod) list(c *views.Context) *utils.Response {
	var ser ListSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":           ser.Name,
		"namespace":      ser.Namespace,
		"label_selector": ser.LabelSelector,
	}
	return p.Pod.List(c.Param("cluster"), reqParams)
}

func (p *Pod) get(c *views.Context) *utils.Response {
	var ser GetSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"output":    ser.Output,
	}
	return p.Pod.Get(c.Param("cluster"), reqParams)
}
