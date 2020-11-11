package router

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/openspacee/osp/pkg/kube_resource"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/redis"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/router/views/ws_views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"k8s.io/klog"
	"net/http"
	"runtime"
	"strings"
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

	kubeMessage := kube_resource.NewMiddleMessage(redisOptions)
	models := model.NewModels(redisOptions)
	kubeResources := kube_resource.NewKubeResources(kubeMessage)

	// 统一认证的api接口
	apiGroup := engine.Group("/api/v1")
	viewsets := NewViewSets(kubeResources, models)
	for group, vs := range *viewsets {
		g := apiGroup.Group(group)
		for _, v := range vs {
			g.Handle(v.Method, v.Path, apiWrapper(models, v.Handler))
		}
	}

	// 登录登出接口
	loginView := views.NewLogin(models)
	apiGroup.POST("/login", loginView.Login)
	apiGroup.GET("/has_admin", loginView.HasAdmin)
	apiGroup.POST("/admin", loginView.CreateAdmin)
	apiGroup.POST("/logout", loginView.Logout)

	// 连接k8s agent的websocket接口
	kubeWs := ws_views.NewKubeWs(redisOptions, models)
	apiGroup.GET("/kube/connect", kubeWs.Connect)

	// 连接api websocket接口
	apiWs := ws_views.NewApiWs(redisOptions, models, kubeResources)
	apiGroup.GET("/web/connect", apiWs.Connect)

	// 连接exec websocket接口
	execWs := ws_views.NewExecWs(redisOptions, models, kubeResources)
	apiGroup.GET("/exec/:cluster/:namespace/:pod", execWs.Connect)

	// 连接log websocket接口
	logWs := ws_views.NewLogWs(redisOptions, models, kubeResources)
	apiGroup.GET("/log/:cluster/:namespace/:pod", logWs.Connect)

	return &Router{
		Engine: engine,
	}
}

func apiWrapper(m *model.Models, handler views.ViewHandler) gin.HandlerFunc {
	return func(c *gin.Context) {
		authRes := auth(m, c)
		if !authRes.IsSuccess() {
			c.JSON(200, authRes)
		} else {
			context := &views.Context{Context: c, UserName: authRes.Data.(map[string]interface{})["name"].(string)}
			res := handler(context)
			c.JSON(200, res)
		}
	}
}

func auth(m *model.Models, c *gin.Context) *utils.Response {
	resp := utils.Response{Code: code.Success}
	token := c.DefaultQuery("token", "")
	if token == "" {
		token = c.Request.Header.Get("Authorization")
		if s := strings.Split(token, " "); len(s) == 2 {
			token = s[1]
		}
	}
	if token == "" {
		resp.Code = code.ParamsError
		resp.Msg = "not found token"
		return &resp
	}

	tk, err := m.TokenManager.Get(token)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = err.Error()
		return &resp
	}

	u, err := m.UserManager.Get(tk.UserName)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = err.Error()
		return &resp
	}
	resp.Data = map[string]interface{}{
		"name": u.Name,
		"password": u.Password,
	}
	return &resp
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
