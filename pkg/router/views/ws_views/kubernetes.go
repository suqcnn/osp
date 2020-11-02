package ws_views

import (
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/openspacee/osp/pkg/redis"
	kubewebsocket "github.com/openspacee/osp/pkg/websockets"
	"k8s.io/klog"
)

type KubeWs struct {
	redisOptions *redis.Options
}

func NewKubeWs(op *redis.Options) *KubeWs {
	return &KubeWs{
		redisOptions: op,
	}
}

func (k *KubeWs) Connect(c *gin.Context) {
	cluster := "aaa"
	upGrader := &websocket.Upgrader{}
	ws, err := upGrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		klog.Errorf("upgrader agent conn error: %s", err)
		return
	}
	token := c.GetHeader("token")
	klog.Info(token)

	kubeWebsocket := kubewebsocket.NewKubeWebsocket(cluster, ws, k.redisOptions)
	kubeWebsocket.Consume()
	klog.Infof("cluster %s kube connect finish", cluster)
}
