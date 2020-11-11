package views

import (
	"fmt"
	"github.com/google/uuid"
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/model/types"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"net/http"
)

type Cluster struct {
	Views  []*View
	models *model.Models
	*kube_resource.KubeResources
}

func NewCluster(models *model.Models, kr *kube_resource.KubeResources) *Cluster {
	cluster := &Cluster{
		models:        models,
		KubeResources: kr,
	}
	views := []*View{
		NewView(http.MethodGet, "", cluster.list),
		NewView(http.MethodPost, "", cluster.create),
		NewView(http.MethodGet, "/:cluster/detail", cluster.detail),
	}
	cluster.Views = views
	return cluster
}

func (clu *Cluster) list(c *Context) *utils.Response {
	resp := &utils.Response{Code: code.Success}
	var filters map[string]interface{}
	clus, err := clu.models.ClusterManager.List(filters)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = err.Error()
		return resp
	}
	var data []map[string]interface{}

	for _, du := range clus {
		data = append(data, map[string]interface{}{
			"name": du.Name,
			"token": du.Token.String(),
			"status": du.Status,
			"create_time": du.CreateTime,
			"update_time": du.UpdateTime,
		})
	}
	resp.Data = data
	return resp
}

func (clu *Cluster) create(c *Context) *utils.Response {
	var ser ClusterCreateSerializers
	resp := &utils.Response{Code: code.Success}

	if err := c.ShouldBind(&ser); err != nil {
		resp.Code = code.ParamsError
		resp.Msg = err.Error()
		return resp
	}
	if ser.Name == "" {
		resp.Code = code.ParamsError
		resp.Msg = fmt.Sprintf("params cluster name:%s blank", ser.Name)
		return resp
	}
	cluster := &types.Cluster{
		Name: ser.Name,
		Token: uuid.New(),
		Status: "normal",
	}
	cluster.CreateTime = utils.StringNow()
	cluster.UpdateTime = utils.StringNow()
	if err := clu.models.ClusterManager.Create(cluster); err != nil {
		resp.Code = code.CreateError
		resp.Msg = err.Error()
		return resp
	}
	return resp
}

func (clu *Cluster) detail(c *Context) *utils.Response {
	return clu.Cluster.Get(c.Param("cluster"), map[string]interface{}{})
}
