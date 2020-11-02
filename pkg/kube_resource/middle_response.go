package kube_resource

import "encoding/json"

type MiddleResponse struct {
	RequestId    string      `json:"request_id"`
	Data         interface{} `json:"data"`
	ResponseType string      `json:"response_type"`
}

func NewMiddleResponse(reqId, resType string, data interface{}) *MiddleResponse {
	return &MiddleResponse{
		RequestId:    reqId,
		Data:         data,
		ResponseType: resType,
	}
}

func UnserialzerMiddleResponse(d string) (*MiddleResponse, error) {
	var mr MiddleResponse
	err := json.Unmarshal([]byte(d), &mr)
	if err != nil {
		return nil, err
	}
	return &mr, nil
}

func (m *MiddleResponse) Serializer() ([]byte, error) {
	return json.Marshal(m.Data)
}
