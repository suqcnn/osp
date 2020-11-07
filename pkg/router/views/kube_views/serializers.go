package kube_views

type ListSerializers struct {
	Cluster       string      `json:"cluster" form:"cluster"`
	Name          string      `json:"name" form:"name"`
	Namespace     string      `json:"namespace" form:"namespace"`
	LabelSelector interface{} `json:"label_selector" form:"label_selector"`
}

type GetSerializers struct {
	Cluster   string `json:"cluster" form:"cluster"`
	Name      string `json:"name" form:"name"`
	Namespace string `json:"namespace" form:"namespace"`
	Output    string `json:"output" form:"output"`
	Kind      string `json:"kind" form:"kind"`
}

type DeleteResource struct {
	Name      string `json:"name"`
	Namespace string `json:"namespace"`
}

type DeleteSerializers struct {
	Resources []DeleteResource `json:"resources"`
}

type UpdateSerializers struct {
	Yaml string `json:"yaml"`
	Kind string `json:"kind"`
}

type UpdateWorkloadSerializers struct {
	Replicas int `json:"replicas" form:"replicas"`
}

type EventListSerializers struct {
	UID       string `json:"uid" form:"uid"`
	Kind      string `json:"kind" form:"kind"`
	Name      string `json:"name" form:"name"`
	Namespace string `json:"namespace" form:"namespace"`
}
