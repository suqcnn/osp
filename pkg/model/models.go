package model

import (
	"github.com/openspacee/osp/pkg/model/manager"
	"github.com/openspacee/osp/pkg/redis"
)

type Models struct {
	*manager.ClusterManager
	*manager.UserManager
	*manager.TokenManager
}

func NewModels(redisOp *redis.Options) *Models {
	client := redis.NewRedisClient(redisOp)
	cm := manager.NewClusterManager(client)
	user := manager.NewUserManager(client)
	tk := manager.NewTokenManager(client)

	return &Models{
		ClusterManager: cm,
		UserManager: user,
		TokenManager: tk,
	}
}
