package views

import (
	"github.com/openspacee/osp/pkg/utils"
	"github.com/openspacee/osp/pkg/utils/code"
	"net/http"
)

type User struct {
	Views []*View
}

func NewUser() *User {
	user := &User{}
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
