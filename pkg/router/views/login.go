package views

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/model/types"
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

	userObj, err := l.models.UserManager.Get(user.UserName)
	if err != nil {
		resp.Code = code.GetError
		resp.Msg = fmt.Sprintf("not found user by name:%s", user.UserName)
		c.JSON(http.StatusOK, resp)
		return
	}

	if password != userObj.Password {
		resp.Code = code.AuthError
		resp.Msg = fmt.Sprintf("password error for user by:%s", user.UserName)
		c.JSON(http.StatusOK, resp)
		return
	}

	tkObj := types.Token{
		UserName: user.UserName,
		Token: uuid.New(),
	}
	if err := l.models.TokenManager.Create(&tkObj); err != nil  {
		resp.Code = code.CreateError
		resp.Msg = fmt.Sprintf("create token for user:%s error:%s", user.UserName, err.Error())
		c.JSON(http.StatusOK, resp)
		return
	}

	userObj.LastLogin = utils.StringNow()
	if err := l.models.UserManager.Update(userObj); err != nil {
		resp.Code = code.UpdateError
		resp.Msg = err.Error()
		c.JSON(http.StatusOK, resp)
		return
	}
	resp.Data = map[string]interface{}{
		"token": tkObj.Token.String(),
	}
	c.Set("user", user)
	c.JSON(http.StatusOK, resp)
}

func (l Login) HasAdmin(c *gin.Context) {
	data := map[string]interface{}{
		"has": 1,
	}
	if _, err := l.models.UserManager.Get("admin"); err != nil {
		data["has"] = 0
	}
	c.JSON(http.StatusOK, &utils.Response{Code: code.Success, Data: data})
}


func (l Login) CreateAdmin(c *gin.Context) {
	var ser UserCreateSerializers
	resp := &utils.Response{Code: code.Success}
	if err := c.ShouldBind(&ser); err != nil {
		resp.Code = code.ParamsError
		resp.Msg = err.Error()
		c.JSON(http.StatusOK, resp)
		return
	}

	user := types.User{
		Name: "admin",
		Email: ser.Email,
		Password: utils.Encrypt(ser.Password),
		Status: "normal",
	}
	user.CreateTime = utils.StringNow()
	user.UpdateTime = utils.StringNow()

	if err := l.models.UserManager.Create(&user); err != nil {
		resp.Code = code.CreateError
		resp.Msg = err.Error()
		c.JSON(http.StatusOK, resp)
		return
	}

	resp.Data = map[string]interface{}{
		"name": user.Name,
		"password": user.Password,
	}
	c.JSON(http.StatusOK, resp)
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