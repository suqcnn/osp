package manager

import (
	"context"
	"github.com/go-redis/redis/v8"
)

type UserManager struct {
	CommonManager
}

func NewUserManager(redisClient *redis.Client) *UserManager {
	return &UserManager{
		CommonManager{
			client: redisClient,
			modelKey: "osp:user",
			Context: context.Background(),
		},
	}
}
