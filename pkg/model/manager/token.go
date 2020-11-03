package manager

import (
	"github.com/go-redis/redis/v8"
	"github.com/openspacee/osp/pkg/model/types"
)

type TokenManager struct {
	client *redis.Client
}

func NewTokenManager(redisClient *redis.Client) *TokenManager {
	return &TokenManager{
		client: redisClient,
	}
}

func (tm *TokenManager) List() ([]*types.Token, error) {
	return nil, nil
}
