package types

const (
	ClusterPending = "Pending"
	ClusterConnect = "Connect"
)

type Cluster struct {
	Common

	Name   string `json:"name"`
	Token  string `json:"token"`
	Status string `json:"status"`
}
