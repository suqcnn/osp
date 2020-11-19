package manager

import (
	"context"
	"encoding/json"
	"github.com/go-redis/redis/v8"
	"github.com/openspacee/osp/pkg/model/types"
)

type ClusterManager struct {
	CommonManager
}

func NewClusterManager(redisClient *redis.Client) *ClusterManager {
	return &ClusterManager{
		CommonManager{
			client:   redisClient,
			modelKey: "osp:cluster",
			Context:  context.Background(),
		},
	}
}

func (clu *ClusterManager) Create(cluster *types.Cluster) error {
	if err := clu.CommonManager.Save(cluster.Name, cluster, -1, true); err != nil {
		return err
	}

	return nil
}

func (clu *ClusterManager) List(filters map[string]interface{}) ([]*types.Cluster, error) {
	dList, err := clu.CommonManager.List(filters)
	if err != nil {
		return nil, err
	}
	jsonBody, err := json.Marshal(dList)
	if err != nil {
		return nil, err
	}
	var clus []*types.Cluster

	if err := json.Unmarshal(jsonBody, &clus); err != nil {
		return nil, err
	}
	return clus, nil
}

func (clu *ClusterManager) GetByToken(token string) (*types.Cluster, error) {

	clusterList, err := clu.List(map[string]interface{}{
		"token": token,
	})
	if err != nil {
		return nil, err
	}
	for _, clu := range clusterList {
		if clu.Token.String() == token {
			return clu, nil
		}
	}
	return nil, nil
}
