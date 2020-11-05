package ws_views

import (
	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/redis"
	kubewebsocket "github.com/openspacee/osp/pkg/websockets"
	"k8s.io/klog"
	"net/http"
)

type LogWs struct {
	redisOptions *redis.Options
	models       *model.Models
	*kube_resource.KubeResources
}

func NewLogWs(op *redis.Options, models *model.Models, kr *kube_resource.KubeResources) *LogWs {
	return &LogWs{
		redisOptions:  op,
		models:        models,
		KubeResources: kr,
	}
}

func (l *LogWs) Connect(c *gin.Context) {
	upGrader := &websocket.Upgrader{}
	upGrader.CheckOrigin = func(r *http.Request) bool { return true }
	ws, err := upGrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		klog.Errorf("upgrader agent conn error: %s", err)
		return
	}
	token := c.GetHeader("token")
	klog.Info(token)

	container := c.Query("container")

	cluster, ok := c.Params.Get("cluster")
	if !ok {
		ws.WriteMessage(websocket.TextMessage, []byte("get cluster params error"))
		ws.Close()
		return
	}
	namespace, ok := c.Params.Get("namespace")
	if !ok {
		ws.WriteMessage(websocket.TextMessage, []byte("get namespace params error"))
		ws.Close()
		return
	}
	pod, ok := c.Params.Get("pod")
	if !ok {
		ws.WriteMessage(websocket.TextMessage, []byte("get pod params error"))
		ws.Close()
		return
	}

	logWebsocket := kubewebsocket.NewLogWebsocket(cluster, ws, l.redisOptions, l.KubeResources,
		namespace, pod, container)
	go logWebsocket.Consume()
	klog.Info("log websocket connect finish")
}
