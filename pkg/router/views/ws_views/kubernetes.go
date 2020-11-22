package ws_views

import (
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/redis"
	kubewebsocket "github.com/openspacee/osp/pkg/websockets"
	"k8s.io/klog"
)

type KubeWs struct {
	redisOptions *redis.Options
	models       *model.Models
}

func NewKubeWs(op *redis.Options, models *model.Models) *KubeWs {
	return &KubeWs{
		redisOptions: op,
		models:       models,
	}
}

func (k *KubeWs) Connect(c *gin.Context) {

	token := c.GetHeader("token")
	klog.Info(token)

	cluster, err := k.models.ClusterManager.GetByToken(token)
	if err != nil {
		klog.Errorf("get cluster error")
		return
	}
	if cluster == nil {
		klog.Errorf("can not get cluster")
		return
	}

	upGrader := &websocket.Upgrader{}
	ws, err := upGrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		klog.Errorf("upgrader agent conn error: %s", err)
		return
	}
	klog.Info(cluster.Name)
	kubeWebsocket := kubewebsocket.NewKubeWebsocket(cluster.Name, ws, k.redisOptions)
	kubeWebsocket.Consume()
	klog.Infof("cluster %s kube connect finish", cluster.Name)
}
