package views

import (
	"fmt"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/model/types"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"net/http"
)

type User struct {
	Views  []*View
	models *model.Models
}

func NewUser(models *model.Models) *User {
	user := &User{
		models: models,
	}
	views := []*View{
		NewView(http.MethodGet, "", user.list),
		NewView(http.MethodPost, "", user.create),
		NewView(http.MethodPut, "/:username", user.update),

		NewView(http.MethodGet, "/token", user.tokenUser),

	}
	user.Views = views
	return user
}

func (u *User) tokenUser(c *Context) *utils.Response {
	return &utils.Response{Code: code.Success,
		Data: map[string]interface{}{
			"name": c.User.Name,
		},
	}
}

func (u *User) update(c *Context) *utils.Response {
	userName := c.Param("username")
	var user UserSerializers
	resp := utils.Response{Code: code.Success}
	if err := c.ShouldBindJSON(&user); err != nil {
		resp.Code = code.ParamsError
		resp.Msg = err.Error()
		return &resp
	}

	userObj := types.User{}
	if err := u.models.UserManager.Get(userName, &userObj); err != nil {
		resp.Code = code.GetError
		resp.Msg = fmt.Sprintf("not found user:%s", userName)
		return &resp
	}

	if user.Status != "" {
		userObj.Status = user.Status
	}

	if user.Email != "" {
		userObj.Email = user.Email
	}

	if err := u.models.UserManager.Save(userObj.Name, &userObj, -1, false); err != nil {
		resp.Code = code.CreateError
		resp.Msg = err.Error()
		return &resp
	}
	return &resp
}

func (u *User) list(c *Context) *utils.Response {
	resp := utils.Response{Code: code.Success}
	var filters map[string]string

	dList, err := u.models.UserManager.List(filters)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = err.Error()
		return &resp
	}
	var data []map[string]interface{}

	for _, du := range dList {
		data = append(data, map[string]interface{}{
			"name": du["name"],
			"email": du["email"],
			"status": du["status"],
			"last_login": du["last_login"],
		})
	}
	resp.Data = data
	return &resp
}

func (u *User) create(c *Context) *utils.Response {
	var ser UserCreateSerializers
	if err := c.ShouldBind(&ser); err != nil {
		return &utils.Response{Code: code.ParamsError, Msg: err.Error()}
	}
	user := &types.User{
		Name: ser.Name,
		Email: ser.Email,
		Password: utils.Encrypt(ser.Password),
		Status: "normal",
		LastLogin: utils.StringNow(),
	}
	user.CreateTime = utils.StringNow()
	user.UpdateTime = utils.StringNow()

	if err := u.models.UserManager.Save(user.Name, user, -1, true); err != nil {
		return &utils.Response{Code: code.CreateError, Msg: err.Error()}
	}
	return &utils.Response{Code: code.Success, Data: map[string]interface{}{
		"name": user.Name,
		"email": user.Email,
		"status": user.Status,
	}}
}
