package router

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/redis"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/router/views/kube_views"
)

type ViewSets map[string][]*views.View

func NewViewSets(redisOptions *redis.Options, models *model.Models) *ViewSets {
	viewsets := make(ViewSets)
	kubeMessage := kube_resource.NewMiddleMessage(redisOptions)

	cluster := views.NewCluster(models)
	viewsets["cluster"] = cluster.Views

	user := views.NewUser(models)
	viewsets["user"] = user.Views

	pods := kube_views.NewPod(kubeMessage)
	viewsets["pods"] = pods.Views

	return &viewsets
}
