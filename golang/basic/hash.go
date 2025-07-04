package main

import (
	"crypto/md5"
	"crypto/sha1"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"hash"
	"math/big"
)

func hashToHex(str string, hfunc hash.Hash) string {
	hfunc.Write([]byte(str))
	hashValue := hfunc.Sum(nil)
	return hex.EncodeToString(hashValue)
}

func main() {
	var str string = "hello world"

	// 用法1: 直接使用Sum函数
	md5Hash := md5.Sum([]byte(str))
	sha1Hash := sha1.Sum([]byte(str))
	sha256Hash := sha256.Sum256([]byte(str))

	fmt.Println("md5Hash:\t", hex.EncodeToString(md5Hash[:]), new(big.Int).SetBytes(md5Hash[:]).Uint64())
	fmt.Println("sha1Hash:\t", hex.EncodeToString(sha1Hash[:]), new(big.Int).SetBytes(sha1Hash[:]).Uint64())
	fmt.Println("sha256Hash:\t", hex.EncodeToString(sha256Hash[:]), new(big.Int).SetBytes(sha256Hash[:]).Uint64())

	// 用法2: 使用hash.Hash接口
	fmt.Println("md5Hash:\t", hashToHex(str, md5.New()))
	fmt.Println("sha1Hash:\t", hashToHex(str, sha1.New()))
	fmt.Println("sha256Hash:\t", hashToHex(str, sha256.New()))
}
