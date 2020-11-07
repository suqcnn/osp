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
	userObj := types.User{}
	if err := l.models.UserManager.Get(user.UserName, &userObj); err != nil {
		resp.Code = code.DataNotExists
		resp.Msg = fmt.Sprintf("not found user by:%s", user.UserName)
		c.JSON(http.StatusOK, resp)
		return
	}

	if password != userObj.Password {
		resp.Code = code.AuthError
		resp.Msg = fmt.Sprintf("password error for user by:%s", user.UserName)
		c.JSON(http.StatusOK, resp)
		return
	}

	tk := uuid.New()
	tkObj := &types.Token{
		UserName: user.UserName,
		Token: tk,
	}
	tkObj.CreateTime = utils.StringNow()
	tkObj.UpdateTime = utils.StringNow()

	if err := l.models.TokenManager.Save(tkObj.Token.String(), tkObj, 43200, false); err != nil {
		resp.Code = code.CreateError
		resp.Msg = fmt.Sprintf("create token for user:%s error:%s", tkObj.UserName, err.Error())
		c.JSON(http.StatusOK, resp)
		return
	}
	userObj.LastLogin = utils.StringNow()
	if err := l.models.UserManager.Save(userObj.Name, userObj, 0, false); err != nil {
		resp.Code = code.CreateError
		resp.Msg = fmt.Sprintf("create token for user:%s error:%s", tkObj.UserName, err.Error())
		c.JSON(http.StatusOK, resp)
		return
	}
	resp.Data = map[string]interface{}{
		"token": tkObj.Token,
	}
	c.JSON(http.StatusOK, resp)
}

func (l Login) HasAdmin(c *gin.Context) {
	data := map[string]interface{}{
		"has": 1,
	}
	userObj := types.User{}
	if err := l.models.UserManager.Get("admin", &userObj); err != nil {
		data["has"] = 0
		c.JSON(http.StatusOK, &utils.Response{Code: code.Success, Data: data})
	}
	c.JSON(http.StatusOK, &utils.Response{Code: code.Success, Data: data})
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