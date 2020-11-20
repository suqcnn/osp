package kube_views

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/ospagent/pkg/utils/code"
	"net/http"
)

type PV struct {
	Views []*views.View
	*kube_resource.KubeResources
}

func NewPV(kr *kube_resource.KubeResources) *PV {
	pv := &PV{
		KubeResources: kr,
	}
	vs := []*views.View{
		views.NewView(http.MethodGet, "/:cluster/:name", pv.get),
		views.NewView(http.MethodGet, "/:cluster", pv.list),
		views.NewView(http.MethodPost, "/:cluster/delete", pv.delete),
		views.NewView(http.MethodPost, "/:cluster/update/:name", pv.updateYaml),
	}
	pv.Views = vs
	return pv
}

func (pv *PV) list(c *views.Context) *utils.Response {
	var ser ListSerializers
	if err := c.ShouldBindQuery(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      ser.Name,
		"namespace": ser.Namespace,
	}
	return pv.PV.List(c.Param("cluster"), reqParams)
}

func (pv *PV) get(c *views.Context) *utils.Response {
	var ser GetSerializers
	if err := c.ShouldBindQuery(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"output":    ser.Output,
	}
	return pv.PV.Get(c.Param("cluster"), reqParams)
}

func (pv *PV) delete(c *views.Context) *utils.Response {
	var ser DeleteSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	return pv.PV.Delete(c.Param("cluster"), ser)
}

func (pv *PV) updateYaml(c *views.Context) *utils.Response {
	var ser UpdateSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	reqParams := map[string]interface{}{
		"name":      c.Param("name"),
		"namespace": c.Param("namespace"),
		"yaml":      ser.Yaml,
	}
	return pv.PV.UpdateYaml(c.Param("cluster"), reqParams)
}
