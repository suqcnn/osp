package manager

import (
	"context"
	"github.com/go-redis/redis/v8"
	"github.com/openspacee/osp/pkg/model/types"
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

func (u *UserManager) Get(name string) (*types.User, error) {
	userObj := types.User{}
	if err := u.CommonManager.Get(name, &userObj); err != nil {
		return nil, err
	}
	return &userObj, nil
}

func (u *UserManager) Update(user *types.User) error {
	if err := u.CommonManager.Save(user.Name, user, 0, false); err != nil {
		return err
	}
	return nil
}

func (u *UserManager) Create(user *types.User) error {

	if err := u.CommonManager.Save(user.Name, user, -1, true); err != nil {
		return err
	}
	return nil
}