package main

import (
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"hash"
)

func hashFunc(str string, hfunc hash.Hash) string {
	hfunc.Write([]byte(str))
	hashValue := hfunc.Sum(nil)
	return hex.EncodeToString(hashValue)
}

func main() {
	var str string = "hello world"
	fmt.Println("md5Hash:\t", hashFunc(str, md5.New()))
	fmt.Println("sha1Hash:\t", hashFunc(str, sha1.New()))
	fmt.Println("sha256Hash:\t", hashFunc(str, sha256.New()))
}
