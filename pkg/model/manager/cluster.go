package manager

import (
	"context"
	"github.com/go-redis/redis/v8"
)

type ClusterManager struct {
	CommonManager
}

func NewClusterManager(redisClient *redis.Client) *ClusterManager {
	return &ClusterManager{
		CommonManager{
			client:   redisClient,
			modelKey: "osp:cluster",
			Context: context.Background(),
		},
	}
}
