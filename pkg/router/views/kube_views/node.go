package kube_views

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/utils"
	"net/http"
)

type Node struct {
	Views []*views.View
	*kube_resource.KubeResources
}

func NewNode(kr *kube_resource.KubeResources) *Node {
	node := &Node{
		KubeResources: kr,
	}
	vs := []*views.View{
		views.NewView(http.MethodGet, "/:cluster", node.list),
	}
	node.Views = vs
	return node
}

func (n *Node) list(c *views.Context) *utils.Response {
	return n.Node.List(c.Param("cluster"), struct{}{})
}
