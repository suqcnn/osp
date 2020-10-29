package utils

import "github.com/google/uuid"

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
