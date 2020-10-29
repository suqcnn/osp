package core

import (
	"github.com/openspacee/osp/pkg/options"
	"github.com/openspacee/osp/pkg/redis"
)

type ServerConfig struct {
	Port         int
	RedisOptions *redis.Options
}

func NewServerConfig(op *options.ServerOptions) (*ServerConfig, error) {
	redisOp := &redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	}
	return &ServerConfig{
		Port:         op.Port,
		RedisOptions: redisOp,
	}, nil
}
