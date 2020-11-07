package views

type UserCreateSerializers struct {
	Name      string `json:"name"`
	Email     string `json:"email"`
	Password  string `json:"password"`
}

type UserSerializers struct {
	UserName  string `json:"username"`
	Password  string `json:"password"`
	Email     string `json:"email"`
	Status    string `json:"status"`
}

