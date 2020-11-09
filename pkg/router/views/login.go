package views

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"net/http"
	"strings"
)

type Login struct {
	models *model.Models
}

func NewLogin(models *model.Models) *Login {
	return &Login{
		models: models,
	}
}

func (l Login) Login(c *gin.Context) {
	var user UserSerializers
	resp := &utils.Response{Code: code.Success}
	if err := c.ShouldBindJSON(&user); err != nil {
		resp.Code = code.ParamsError
		resp.Msg = err.Error()
		c.JSON(http.StatusOK, resp)
		return
	}
	if user.UserName == "" || user.Password == "" {
		resp.Code = code.ParamsError
		resp.Msg = fmt.Sprintf("username:%s password:%s blank", user.UserName, user.Password)
		c.JSON(http.StatusOK, resp)
		return
	}
	password := utils.Encrypt(user.Password)

	up := l.models.UserManager.Get(user.UserName)
	if !up.IsSuccess() {
		c.JSON(http.StatusOK, up)
		return
	}

	userObjPassword := up.Data.(map[string]interface{})["password"].(string)
	if password != userObjPassword {
		resp.Code = code.AuthError
		resp.Msg = fmt.Sprintf("password error for user by:%s", user.UserName)
		c.JSON(http.StatusOK, resp)
		return
	}

	tk := l.models.TokenManager.Create(user.UserName)
	if !tk.IsSuccess() {
		resp.Code = code.CreateError
		resp.Msg = fmt.Sprintf("create token for user:%s error:%s", user.UserName, tk.Msg)
		c.JSON(http.StatusOK, resp)
		return
	}

	params := map[string]interface{}{
		"last_login": utils.StringNow(),
	}
	up = l.models.UserManager.Update(user.UserName, params)
	if !up.IsSuccess() {
		c.JSON(http.StatusOK, up)
		return
	}
	resp.Data = map[string]interface{}{
		"token": tk.Data.(map[string]interface{})["token"].(string),
	}
	c.JSON(http.StatusOK, resp)
}

func (l Login) HasAdmin(c *gin.Context) {
	data := map[string]interface{}{
		"has": 1,
	}
	up := l.models.UserManager.Get("admin")
	if !up.IsSuccess() {
		data["has"] = 0
	}
	c.JSON(http.StatusOK, &utils.Response{Code: code.Success, Data: data})
}


func (l Login) CreateAdmin(c *gin.Context) {
	var ser UserCreateSerializers
	if err := c.ShouldBind(&ser); err != nil {
		c.JSON(http.StatusOK, &utils.Response{Code: code.ParamsError, Msg: err.Error()})
		return
	}

	params := map[string]interface{}{
		"name": "admin",
		"email": ser.Email,
		"password": ser.Password,
	}

	uc := l.models.UserManager.Create(params)
	if !uc.IsSuccess() {
		c.JSON(http.StatusOK, uc)
		return
	}

	c.JSON(http.StatusOK, &utils.Response{
		Code: code.Success,
		Data: uc.Data,
	})
}

func (l Login) Logout(c *gin.Context) {
	resp := &utils.Response{Code: code.Success}
	token := l.GetToken(c)
	if token != "" {
		if err := l.models.TokenManager.Delete(token); err != nil {
			resp.Code = code.DeleteError
			resp.Msg = err.Error()
		}
	}
	c.JSON(http.StatusOK, resp)
}

func (l Login) GetToken(c *gin.Context) string {
	token := c.Request.Header.Get("Authorization")
	if s := strings.Split(token, " "); len(s) == 2 {
		token = s[1]
	}
	return token
}