package core

import (
	"github.com/openspacee/osp/pkg/options"
	"github.com/openspacee/osp/pkg/redis"
	"github.com/openspacee/osp/pkg/utils"
	"time"
)

type ServerConfig struct {
	Port         int
	RedisOptions *redis.Options
	CertFilePath string
	KeyFilePath  string
}

func NewServerConfig(op *options.ServerOptions) (*ServerConfig, error) {
	redisOp := &redis.Options{
		Addr:     op.RedisAddress,
		Password: op.RedisPassword,
		DB:       op.RedisDB,
	}
	certFilePath := op.CertFilePath
	keyFilePath := op.KeyFilePath
	if op.CertFilePath == "" || op.KeyFilePath == "" {
		err := utils.GenerateCert("localhost,127.0.0.1,*", time.Hour*24*365*10, true, "P256")
		if err != nil {
			return nil, err
		}
		certFilePath = "cert.pem"
		keyFilePath = "key.pem"
	}
	return &ServerConfig{
		Port:         op.Port,
		RedisOptions: redisOp,
		CertFilePath: certFilePath,
		KeyFilePath:  keyFilePath,
	}, nil
}
