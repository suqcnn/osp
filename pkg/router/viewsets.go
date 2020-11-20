package router

import (
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/router/views/kube_views"
)

type ViewSets map[string][]*views.View

func NewViewSets(kr *kube_resource.KubeResources, models *model.Models) *ViewSets {
	cluster := views.NewCluster(models, kr)
	user := views.NewUser(models)

	pods := kube_views.NewPod(kr)
	event := kube_views.NewEvent(kr)
	namespace := kube_views.NewNamespace(kr)
	deployment := kube_views.NewDeployment(kr)
	node := kube_views.NewNode(kr)
	statefulset := kube_views.NewStatefulset(kr)
	daemonset := kube_views.NewDaemonset(kr)
	cronjob := kube_views.NewCronjob(kr)
	job := kube_views.NewJob(kr)
	service := kube_views.NewService(kr)
	endpoints := kube_views.NewEndpoint(kr)
	ingress := kube_views.NewIngress(kr)
	networkpolicy := kube_views.NewNetworkPolicy(kr)
	serviceaccount := kube_views.NewServiceAccount(kr)
	rolebinding := kube_views.NewRolebinding(kr)
	role := kube_views.NewRole(kr)
	configmap := kube_views.NewConfigMap(kr)
	secret := kube_views.NewSecret(kr)
	hpa := kube_views.NewHpa(kr)
	pvc := kube_views.NewPvc(kr)
	pv := kube_views.NewPV(kr)
	storageclass := kube_views.NewStorageClass(kr)

	viewsets := &ViewSets{
		"cluster":        cluster.Views,
		"user":           user.Views,
		"pods":           pods.Views,
		"event":          event.Views,
		"namespace":      namespace.Views,
		"deployment":     deployment.Views,
		"nodes":          node.Views,
		"statefulset":    statefulset.Views,
		"daemonset":      daemonset.Views,
		"cronjob":        cronjob.Views,
		"job":            job.Views,
		"service":        service.Views,
		"endpoints":      endpoints.Views,
		"ingress":        ingress.Views,
		"networkpolicy":  networkpolicy.Views,
		"serviceaccount": serviceaccount.Views,
		"rolebinding":    rolebinding.Views,
		"role":           role.Views,
		"configmap":      configmap.Views,
		"secret":         secret.Views,
		"hpa":            hpa.Views,
		"pvc":            pvc.Views,
		"pv":             pv.Views,
		"storageclass":   storageclass.Views,
	}

	return viewsets
}
