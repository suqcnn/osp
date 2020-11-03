package manager

import (
	"github.com/go-redis/redis/v8"
	"github.com/openspacee/osp/pkg/model/types"
)

type UserManager struct {
	client *redis.Client
}

func NewUserManager(redisClient *redis.Client) *UserManager {
	return &UserManager{
		client: redisClient,
	}
}

func (um *UserManager) List() ([]*types.User, error) {
	return nil, nil
}
