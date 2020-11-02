package views

import (
	"github.com/gin-gonic/gin"
	"github.com/openspacee/osp/pkg/model"
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"net/http"
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
	resp := &utils.Response{Code: code.Success, Data: map[string]interface{}{"token": "1234234"}}
	c.JSON(http.StatusOK, resp)
}

func (l Login) HasAdmin(c *gin.Context) {
	resp := &utils.Response{Code: code.Success, Data: map[string]interface{}{"has": 1}}
	c.JSON(http.StatusOK, resp)
}

func (l Login) Logout(c *gin.Context) {
	resp := &utils.Response{Code: code.Success}
	c.JSON(http.StatusOK, resp)
}
