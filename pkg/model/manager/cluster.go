package manager

import (
	"github.com/go-redis/redis/v8"
	"github.com/openspacee/osp/pkg/model/types"
)

type ClusterManager struct {
	client *redis.Client
}

func NewClusterManager(redisClient *redis.Client) *ClusterManager {
	return &ClusterManager{
		client: redisClient,
	}
}

func (cm *ClusterManager) List() ([]*types.Cluster, error) {
	return nil, nil
}
