package router

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/redis"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/router/views/ws_views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"k8s.io/klog"
	"net/http"
	"runtime"
)

type Router struct {
	*gin.Engine
	viewsets ViewSets
}

func NewRouter(redisOptions *redis.Options) *Router {
	engine := gin.Default()

	engine.Use(LocalMiddleware())

	engine.LoadHTMLFiles("ui/dist/index.html")
	engine.StaticFS("/static", http.Dir("ui/dist/static"))
	engine.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})
	//engine.GET("/ui/login", func(c *gin.Context) {
	//	c.HTML(http.StatusOK, "index.html", nil)
	//})
	engine.GET("/ui/*path", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})

	models := model.NewModels(redisOptions)

	// 统一认证的api接口
	apiGroup := engine.Group("/api/v1")
	viewsets := NewViewSets(redisOptions, models)
	for group, vs := range *viewsets {
		g := apiGroup.Group(group)
		for _, v := range vs {
			g.Handle(v.Method, v.Path, apiWrapper(v.Handler))
		}
	}

	// 登录登出接口
	loginView := views.NewLogin(models)
	apiGroup.POST("/login", loginView.Login)
	apiGroup.GET("/has_admin", loginView.HasAdmin)
	apiGroup.POST("/logout", loginView.Logout)

	// 连接k8s agent的websocket接口
	kubeWs := ws_views.NewKubeWs(redisOptions)
	apiGroup.GET("/kube/connect", kubeWs.Connect)

	return &Router{
		Engine: engine,
	}
}

func apiWrapper(handler views.ViewHandler) gin.HandlerFunc {
	return func(c *gin.Context) {
		authRes := auth(c)
		if !authRes.IsSuccess() {
			c.JSON(200, authRes)
		} else {
			context := &views.Context{Context: c}
			res := handler(context)
			c.JSON(200, res)
		}
	}
}

func auth(c *gin.Context) *utils.Response {
	return &utils.Response{Code: code.Success}
}

func LocalMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {
			if err := recover(); err != nil {
				klog.Error("error: ", err)
				var buf [4096]byte
				n := runtime.Stack(buf[:], false)
				klog.Errorf("==> %s\n", string(buf[:n]))
				msg := fmt.Sprintf("%s", err)
				resp := &utils.Response{Code: code.UnknownError, Msg: msg}
				c.JSON(200, resp)
			}
		}()
		c.Next()
	}
}
