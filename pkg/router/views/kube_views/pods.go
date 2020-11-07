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
		views.NewView(http.MethodGet, "/:cluster/:namespace/:name", pod.get),
		views.NewView(http.MethodPost, "/:cluster/list", pod.list),
		views.NewView(http.MethodPost, "/:cluster/delete", pod.delete),
		views.NewView(http.MethodPost, "/:cluster/update/:namespace/:name", pod.updateYaml),
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
	if err := c.ShouldBindQuery(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"output":    ser.Output,
	}
	return p.Pod.Get(c.Param("cluster"), reqParams)
}

func (p *Pod) delete(c *views.Context) *utils.Response {
	var ser DeleteSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	return p.Pod.Delete(c.Param("cluster"), ser)
}

func (p *Pod) updateYaml(c *views.Context) *utils.Response {
	var ser UpdateSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"yaml":      ser.Yaml,
	}
	return p.Pod.UpdateYaml(c.Param("cluster"), reqParams)
}
