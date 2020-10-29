package utils

import (
	"github.com/openspacee/ospagent/pkg/utils/code"
)

type Response struct {
	Code string      `json:"code"`
	Msg  string      `json:"msg"`
	Data interface{} `json:"data"`
}

func (r *Response) IsSuccess() bool {
	return r.Code == code.Success
}
