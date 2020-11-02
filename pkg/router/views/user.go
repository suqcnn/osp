package views

import (
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
		NewView(http.MethodGet, "/token", user.tokenUser),
	}
	user.Views = views
	return user
}

func (u *User) tokenUser(c *Context) *utils.Response {
	return &utils.Response{Code: code.Success,
		Data: map[string]interface{}{"name": "abc"},
	}
}
