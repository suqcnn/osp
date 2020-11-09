package views

import (
	"fmt"
	"github.com/openspacee/osp/pkg/model"
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
		//NewView(http.MethodPost, "/admin", user.create),
		NewView(http.MethodPut, "/:username", user.update),

		NewView(http.MethodGet, "/token", user.tokenUser),

	}
	user.Views = views
	return user
}

func (u *User) tokenUser(c *Context) *utils.Response {
	return &utils.Response{Code: code.Success,
		Data: map[string]interface{}{
			"name": c.UserName,
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

	params := map[string]interface{}{}

	if user.Status != "" {
		params["status"] = user.Status
	}

	if user.Email != "" {
		if ok := utils.VerifyEmailFormat(user.Email); !ok {
			resp.Code = code.ParamsError
			resp.Msg = fmt.Sprintf("email:%s format error for user:%s", user.Email, userName)
			return &resp
		}
		params["email"] = user.Email
	}

	return u.models.UserManager.Update(userName, params)
}

func (u *User) list(c *Context) *utils.Response {
	resp := utils.Response{Code: code.Success}
	var filters map[string]interface{}

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
	resp := utils.Response{Code: code.Success}

	if err := c.ShouldBind(&ser); err != nil {
		resp.Code = code.ParamsError
		resp.Msg = err.Error()
		return &resp
	}
	if ser.Name == "" {
		ser.Name = "admin"
	} else {
		if ok := utils.VerifyEmailFormat(ser.Email); !ok {
			resp.Code = code.ParamsError
			resp.Msg = fmt.Sprintf("email:%s format error for user:%s", ser.Email, ser.Name)
			return &resp
		}
	}
	params := map[string]interface{}{
		"name": ser.Name,
		"email": ser.Email,
		"password": ser.Password,
	}

	uc := u.models.UserManager.Create(params)
	if !uc.IsSuccess() {
		return uc
	}
	resp.Data = uc.Data
	return &resp
}
