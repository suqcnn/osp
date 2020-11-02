package model

import (
	"github.com/openspacee/osp/pkg/model/manager"
	"github.com/openspacee/osp/pkg/redis"
)

type Models struct {
	*manager.ClusterManager
}

func NewModels(redisOp *redis.Options) *Models {
	client := redis.NewRedisClient(redisOp)
	cm := manager.NewClusterManager(client)

	return &Models{
		ClusterManager: cm,
	}
}
