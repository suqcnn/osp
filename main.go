package main

import (
	"flag"
	"github.com/openspacee/osp/pkg/core"
	"github.com/openspacee/osp/pkg/options"
	"k8s.io/klog"
)

var (
	port          = flag.Int("port", 443, "Server port to listen.")
	redisAddress  = flag.String("redis-address", "localhost:6379", "redis address used.")
	redisDB       = flag.Int("redis-db", 0, "redis db used.")
	redisPassword = flag.String("redis-password", "", "redis password used.")
	certFile      = flag.String("cert-file", "", "cert file path for tls used.")
	keyFile       = flag.String("cert-key-file", "", "cert key file path for tls used.")
)

func createServerOptions() *options.ServerOptions {
	return &options.ServerOptions{
		Port:          *port,
		RedisAddress:  *redisAddress,
		RedisDB:       *redisDB,
		RedisPassword: *redisPassword,
		CertFilePath:  *certFile,
		KeyFilePath:   *keyFile,
	}
}

func buildServer() (*core.Server, error) {
	serverOptions := createServerOptions()
	serverConfig, err := core.NewServerConfig(serverOptions)
	if err != nil {
		klog.Error("New server config error:", err)
		return nil, err
	}
	return core.NewServer(serverConfig), nil
}

func main() {
	klog.InitFlags(nil)
	flag.Parse()
	flag.VisitAll(func(flag *flag.Flag) {
		klog.Infof("FLAG: --%s=%q", flag.Name, flag.Value)
	})
	server, err := buildServer()
	if err != nil {
		panic(err)
	}
	server.Run()
}
