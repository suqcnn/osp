package manager

import (
	"context"
	"fmt"
	"github.com/go-redis/redis/v8"
	"github.com/openspacee/osp/pkg/model/types"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
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

func (u *UserManager) Get(name string) *utils.Response {
	resp := utils.Response{Code: code.Success}
	userObj := types.User{}
	if err := u.CommonManager.Get(name, &userObj); err != nil {
		resp.Code = code.DataNotExists
		resp.Msg = fmt.Sprintf("not found user by:%s", name)
		return &resp
	}

	resp.Data = map[string]interface{}{
		"name": userObj.Name,
		"password": userObj.Password,
	}
	return &resp
}

func (u *UserManager) Update(name string, params map[string]interface{}) *utils.Response {
	resp := utils.Response{Code: code.Success}

	userObj := types.User{}
	if err := u.CommonManager.Get(name, &userObj); err != nil {
		resp.Code = code.DataNotExists
		resp.Msg = fmt.Sprintf("not found user by:%s", name)
		return &resp
	}

	if status, ok := params["status"]; ok {
		userObj.Status = status.(string)
	}
	if email, ok := params["email"]; ok {
		userObj.Email = email.(string)
	}
	if lg, ok := params["last_login"].(string); ok {
		userObj.LastLogin = lg
	}

	if err := u.CommonManager.Save(userObj.Name, userObj, 0, false); err != nil {
		resp.Code = code.UpdateError
		resp.Msg = fmt.Sprintf("update user:%s error:%s", userObj.Name, err.Error())
		return &resp
	}
	return &resp
}

func (u *UserManager) Create(params map[string]interface{}) *utils.Response {
	resp := utils.Response{Code: code.Success}
	user := &types.User{
		Name: params["name"].(string),
		Email: params["email"].(string),
		Password: utils.Encrypt(params["password"].(string)),
		Status: "normal",
		LastLogin: utils.StringNow(),
	}
	user.CreateTime = utils.StringNow()
	user.UpdateTime = utils.StringNow()

	if err := u.CommonManager.Save(user.Name, user, -1, true); err != nil {
		resp.Code = code.CreateError
		resp.Msg = err.Error()
		return &resp
	}
	resp.Data = map[string]interface{}{
		"name": user.Name,
		"email": user.Email,
		"status": user.Status,
		"create_time": user.CreateTime,
	}
	return &resp
}