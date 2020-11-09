package manager

import (
	"context"
	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
	"github.com/openspacee/osp/pkg/model/types"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
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

func (clu *ClusterManager) Create(params map[string]interface{}) *utils.Response {
	resp := utils.Response{Code: code.Success}
	cluster := &types.Cluster{
		Name: params["name"].(string),
		Token: uuid.New(),
		Status: "normal",
	}
	cluster.CreateTime = utils.StringNow()
	cluster.UpdateTime = utils.StringNow()

	if err := clu.CommonManager.Save(cluster.Name, cluster, -1, true); err != nil {
		resp.Code = code.CreateError
		resp.Msg = err.Error()
		return &resp
	}

	return &resp
}

func (clu *ClusterManager) List(filters map[string]interface{}) *utils.Response {
	resp := utils.Response{Code: code.Success}

	dList, err := clu.CommonManager.List(filters)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = err.Error()
		return &resp
	}

	var data []map[string]interface{}

	for _, du := range dList {
		data = append(data, map[string]interface{}{
			"name": du["name"],
			"token": du["token"],
			"status": du["status"],
			"create_time": du["create_time"],
			"update_time": du["update_time"],
		})
	}
	resp.Data = data
	return &resp
}