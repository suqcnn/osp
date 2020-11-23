package options

type ServerOptions struct {
	Port          int
	RedisAddress  string
	RedisDB       int
	RedisPassword string
	CertFilePath  string
	KeyFilePath   string
}
