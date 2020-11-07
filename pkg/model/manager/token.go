package manager

import (
	"context"
	"github.com/go-redis/redis/v8"
)

type TokenManager struct {
	CommonManager
}

func NewTokenManager(redisClient *redis.Client) *TokenManager {
	return &TokenManager{
		CommonManager{
			modelKey: "osp:token",
			Context: context.Background(),
			client: redisClient,
		},
	}
}
