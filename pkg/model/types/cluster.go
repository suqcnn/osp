package types

type Cluster struct {
	Common

	Name  string `json:"name"`
	Token string `json:"token"`
}
