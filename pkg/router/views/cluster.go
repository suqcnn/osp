package views

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/model"
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
		NewView(http.MethodGet, "/:cluster/detail", cluster.detail),
	}
	cluster.Views = views
	return cluster
}

func (cluster *Cluster) list(c *Context) *utils.Response {
	return &utils.Response{Code: code.Success,
		Data: []map[string]interface{}{
			{
				"name":  "aaa",
				"token": "we",
			},
		},
	}
}

func (cluster *Cluster) detail(c *Context) *utils.Response {
	return cluster.Cluster.Get(c.Param("cluster"), map[string]interface{}{})
}
