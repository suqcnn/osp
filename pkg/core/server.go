package core

import (
	"fmt"
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
		Addr:    fmt.Sprintf(":%d", s.config.Port),
		Handler: s.router,
	}
	//server.ListenAndServe()
	server.ListenAndServeTLS(s.config.CertFilePath, s.config.KeyFilePath)
}
