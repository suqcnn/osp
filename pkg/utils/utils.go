package utils

import (
	"crypto/md5"
	"encoding/hex"
	"github.com/google/uuid"
	"regexp"
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

func VerifyEmailFormat(email string) bool {
	//pattern := `\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*` //匹配电子邮箱
	pattern := `^[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$`

	reg := regexp.MustCompile(pattern)
	return reg.MatchString(email)
}

//mobile verify
func VerifyMobileFormat(mobileNum string) bool {
	regular := "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"

	reg := regexp.MustCompile(regular)
	return reg.MatchString(mobileNum)
}