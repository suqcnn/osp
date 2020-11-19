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
		//NewView(http.MethodPost, "/admin", user.create),
		NewView(http.MethodPut, "/:username", user.update),

		NewView(http.MethodGet, "/token", user.tokenUser),
	}
	user.Views = views
	return user
}

func (u *User) tokenUser(c *Context) *utils.Response {
	//userName := ""
	//if user, ok := c.Get("user"); ok {
	//	userName = user.(*types.User).Name
	//}
	return &utils.Response{Code: code.Success,
		Data: map[string]interface{}{
			"name": c.UserName,
		}}
}

func (u *User) update(c *Context) *utils.Response {
	userName := c.Param("username")
	var user UserSerializers

	resp := &utils.Response{Code: code.Success}

	if err := c.ShouldBindJSON(&user); err != nil {
		resp.Code = code.ParamsError
		resp.Msg = err.Error()
		return resp
	}

	userObj, err := u.models.UserManager.Get(userName)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = err.Error()
		return resp
	}

	if user.Status != "" {
		userObj.Status = user.Status
	}

	if user.Email != "" {
		if ok := utils.VerifyEmailFormat(user.Email); !ok {
			resp.Code = code.ParamsError
			resp.Msg = fmt.Sprintf("email:%s format error for user:%s", user.Email, userName)
			return resp
		}
		userObj.Email = user.Email
	}

	if err := u.models.UserManager.Update(userObj); err != nil {
		resp.Code = code.UpdateError
		resp.Msg = err.Error()
		return resp
	}
	return resp
}

func (u *User) list(c *Context) *utils.Response {
	resp := &utils.Response{Code: code.Success}
	var filters map[string]interface{}

	dList, err := u.models.UserManager.List(filters)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = err.Error()
		return resp
	}
	var data []map[string]interface{}

	for _, du := range dList {
		data = append(data, map[string]interface{}{
			"name":       du["name"],
			"email":      du["email"],
			"status":     du["status"],
			"last_login": du["last_login"],
		})
	}
	resp.Data = data
	return resp
}

func (u *User) create(c *Context) *utils.Response {
	var ser UserCreateSerializers
	resp := &utils.Response{Code: code.Success}

	if err := c.ShouldBind(&ser); err != nil {
		resp.Code = code.ParamsError
		resp.Msg = err.Error()
		return resp
	}
	if ser.Name == "" {
		ser.Name = "admin"
	} else {
		if ok := utils.VerifyEmailFormat(ser.Email); !ok {
			resp.Code = code.ParamsError
			resp.Msg = fmt.Sprintf("email:%s format error for user:%s", ser.Email, ser.Name)
			return resp
		}
	}

	userObj := types.User{
		Name:     ser.Name,
		Password: utils.Encrypt(ser.Password),
		Email:    ser.Email,
		Status:   "normal",
	}
	userObj.CreateTime = utils.StringNow()
	userObj.UpdateTime = utils.StringNow()

	if err := u.models.UserManager.Create(&userObj); err != nil {
		resp.Code = code.CreateError
		resp.Msg = err.Error()
		return resp
	}

	resp.Data = map[string]interface{}{
		"name":     userObj.Name,
		"password": userObj.Password,
		"status":   userObj.Status,
	}
	return resp
}
