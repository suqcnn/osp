package router

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/openspacee/osp/pkg/redis"
	"github.com/openspacee/osp/pkg/router/views"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"k8s.io/klog"
	"runtime"
)

type Router struct {
	*gin.Engine
	viewsets ViewSets
}

func NewRouter(redisOptions *redis.Options) *Router {
	engine := gin.Default()
	engine.Use(LocalMiddleware())

	apiGroup := engine.Group("/api/v1")
	viewsets := NewViewSets(redisOptions)
	for group, vs := range *viewsets {
		g := apiGroup.Group(group)
		for _, v := range vs {
			g.Handle(v.Method, v.Path, apiWrapper(v.Handler))
		}
	}

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
				resp := &utils.Response{Code: "UnknownError", Msg: msg}
				c.JSON(200, resp)
			}
		}()
		c.Next()
	}
}
