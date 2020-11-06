package kube_views

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/ospagent/pkg/utils/code"
	"net/http"
)

type Job struct {
	Views []*views.View
	*kube_resource.KubeResources
}

func NewJob(kr *kube_resource.KubeResources) *Job {
	d := &Job{
		KubeResources: kr,
	}
	vs := []*views.View{
		views.NewView(http.MethodGet, "/:cluster/:namespace/:name", d.get),
		views.NewView(http.MethodGet, "/:cluster", d.list),
		views.NewView(http.MethodPost, "/:cluster/delete", d.delete),
		views.NewView(http.MethodPost, "/:cluster/update/:namespace/:name", d.updateYaml),
	}
	d.Views = vs
	return d
}

func (d *Job) list(c *views.Context) *utils.Response {
	var ser ListSerializers
	if err := c.ShouldBindQuery(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":           ser.Name,
		"namespace":      ser.Namespace,
		"label_selector": ser.LabelSelector,
	}
	return d.Job.List(c.Param("cluster"), reqParams)
}

func (d *Job) get(c *views.Context) *utils.Response {
	var ser GetSerializers
	if err := c.ShouldBindQuery(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"output":    ser.Output,
	}
	return d.Job.Get(c.Param("cluster"), reqParams)
}

func (d *Job) delete(c *views.Context) *utils.Response {
	var ser DeleteSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	return d.Job.Delete(c.Param("cluster"), ser)
}

func (d *Job) updateYaml(c *views.Context) *utils.Response {
	var ser UpdateSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"yaml":      ser.Yaml,
	}
	return d.Job.UpdateYaml(c.Param("cluster"), reqParams)
}
