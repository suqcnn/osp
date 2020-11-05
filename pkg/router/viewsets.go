package router

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/router/views/kube_views"
)

type ViewSets map[string][]*views.View

func NewViewSets(kr *kube_resource.KubeResources, models *model.Models) *ViewSets {
	viewsets := make(ViewSets)

	cluster := views.NewCluster(models, kr)
	viewsets["cluster"] = cluster.Views

	user := views.NewUser(models)
	viewsets["user"] = user.Views

	pods := kube_views.NewPod(kr)
	viewsets["pods"] = pods.Views

	event := kube_views.NewEvent(kr)
	viewsets["event"] = event.Views

	namespace := kube_views.NewNamespace(kr)
	viewsets["namespace"] = namespace.Views

	return &viewsets
}
