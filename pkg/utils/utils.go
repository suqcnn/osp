package utils

import (
	"crypto/md5"
	"encoding/hex"
	"github.com/google/uuid"
	"time"
)

type Void struct{}

var Ok Void

func Contains(strList []string, str string) bool {
	for _, s := range strList {
		if s == str {
			return true
		}
	}
	return false
}

func int32Ptr(i int32) *int32 { return &i }

func CreateUUID() string {
	return uuid.New().String()
}

func StringNow() string {
	return time.Now().Format("2006-01-02 15:04:05")
}

func Encrypt(key string) string {
	h := md5.New()
	h.Write([]byte(key))
	return hex.EncodeToString(h.Sum(nil))
}