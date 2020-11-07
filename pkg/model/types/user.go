package types

type User struct {
	Common
	Name      string `json:"name"`
	Email     string `json:"email"`
	Password  string `json:"password"`
	Status    string `json:"status"`
	LastLogin string `json:"last_login"`
}
