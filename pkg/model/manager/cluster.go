package manager

import (
	"github.com/go-redis/redis/v8"
	"github.com/openspacee/osp/pkg/model/types"
)

type ClusterManager struct {
	client   *redis.Client
	modelKey string
}

func NewClusterManager(redisClient *redis.Client) *ClusterManager {
	return &ClusterManager{
		client:   redisClient,
		modelKey: "osp:cluster:",
	}
}

func (cm *ClusterManager) List() ([]*types.Cluster, error) {
	return nil, nil
}
