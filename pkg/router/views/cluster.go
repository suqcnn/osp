package views

import (
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"net/http"
)

type Cluster struct {
	Views []*View
}

func NewCluster() *Cluster {
	cluster := &Cluster{}
	views := []*View{
		NewView(http.MethodGet, "", cluster.list),
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
