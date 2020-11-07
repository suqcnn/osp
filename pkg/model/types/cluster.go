package types

import "github.com/google/uuid"

type Cluster struct {
	Common

	Name   string    `json:"name"`
	Token  uuid.UUID `json:"token"`
	Status string    `json:"status"`
}
