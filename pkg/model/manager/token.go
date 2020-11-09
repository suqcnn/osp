package manager

import (
	"context"
	"fmt"
	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
	"github.com/openspacee/osp/pkg/model/types"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
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

func (tk *TokenManager) Create(userName string) *utils.Response {
	resp := utils.Response{Code: code.Success}
	tkId := uuid.New()
	tkObj := &types.Token{
		UserName: userName,
		Token: tkId,
	}
	tkObj.CreateTime = utils.StringNow()
	tkObj.UpdateTime = utils.StringNow()

	if err := tk.CommonManager.Save(tkObj.Token.String(), tkObj, 43200, false); err != nil {
		resp.Code = code.CreateError
		resp.Msg = fmt.Sprintf("create token for user:%s error:%s", tkObj.UserName, err.Error())
		return &resp
	}
	resp.Data = map[string]interface{}{
		"token": tkObj.Token.String(),
	}
	return &resp
}

func (tk *TokenManager) Get(name string) *utils.Response {
	resp := utils.Response{Code: code.Success}
	tkObj := types.Token{}
	if err := tk.CommonManager.Get(name, &tkObj); err != nil {
		resp.Code = code.DataNotExists
		resp.Msg = fmt.Sprintf("not found user by:%s", name)
		return &resp
	}

	resp.Data = map[string]interface{}{
		"username": tkObj.UserName,
		"token": tkObj.Token,
	}
	return &resp
}
