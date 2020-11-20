package kube_views

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/ospagent/pkg/utils/code"
	"net/http"
)

type Pvc struct {
	Views []*views.View
	*kube_resource.KubeResources
}

func NewPvc(kr *kube_resource.KubeResources) *Pvc {
	pvc := &Pvc{
		KubeResources: kr,
	}
	vs := []*views.View{
		views.NewView(http.MethodGet, "/:cluster/:namespace/:name", pvc.get),
		views.NewView(http.MethodGet, "/:cluster", pvc.list),
		views.NewView(http.MethodPost, "/:cluster/delete", pvc.delete),
		views.NewView(http.MethodPost, "/:cluster/update/:namespace/:name", pvc.updateYaml),
	}
	pvc.Views = vs
	return pvc
}

func (p *Pvc) list(c *views.Context) *utils.Response {
	var ser ListSerializers
	if err := c.ShouldBindQuery(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      ser.Name,
		"namespace": ser.Namespace,
	}
	return p.Pvc.List(c.Param("cluster"), reqParams)
}

func (p *Pvc) get(c *views.Context) *utils.Response {
	var ser GetSerializers
	if err := c.ShouldBindQuery(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"output":    ser.Output,
	}
	return p.Pvc.Get(c.Param("cluster"), reqParams)
}

func (p *Pvc) delete(c *views.Context) *utils.Response {
	var ser DeleteSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	return p.Pvc.Delete(c.Param("cluster"), ser)
}

func (p *Pvc) updateYaml(c *views.Context) *utils.Response {
	var ser UpdateSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"yaml":      ser.Yaml,
	}
	return p.Pvc.UpdateYaml(c.Param("cluster"), reqParams)
}
