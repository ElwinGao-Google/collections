package main

import (
	"fmt"
	"log"
	"net/smtp"
)

func main() {
	// 发件人邮箱和授权码 (应用密码)
	fromEmail := "support@sandwichlab.ai"
	appPassword := "jpri vyqo ugrc gljy"

	// 收件人邮箱
	toEmail := "gaowei@sandwichlab.ai"
	recipients := []string{toEmail}

	// Gmail SMTP 服务器配置
	smtpHost := "smtp.gmail.com"
	smtpPort := "587"
	smtpAddr := smtpHost + ":" + smtpPort

	// 1. 设置认证信息
	auth := smtp.PlainAuth("", fromEmail, appPassword, smtpHost)

	// 2. 构建邮件内容 (手动拼接 header 和 body)
	subject := "Subject: Hello from Golang! (via net/smtp)\n"
	mime := "MIME-version: 1.0;\nContent-Type: text/html; charset=\"UTF-8\";\n\n"
	body := "<html><body>This is a test email sent from a Go program using the standard library.</body></html>"

	message := []byte(subject + mime + body)

	// 3. 发送邮件
	if err := smtp.SendMail(smtpAddr, auth, fromEmail, recipients, message); err != nil {
		log.Fatalf("Failed to send email: %v", err)
	}

	fmt.Println("Email sent successfully using net/smtp!")
}
