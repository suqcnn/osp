package core

import (
	"github.com/openspacee/osp/pkg/router"
	"net/http"
)

type Server struct {
	config *ServerConfig
	router *router.Router
}

func NewServer(config *ServerConfig) *Server {
	r := router.NewRouter(config.RedisOptions)
	return &Server{
		config: config,
		router: r,
	}
}

func (s *Server) Run() {
	server := &http.Server{
		Addr:    ":8080",
		Handler: s.router,
	}
	server.ListenAndServe()
}
