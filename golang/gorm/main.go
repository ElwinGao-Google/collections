package main

import (
	"fmt"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Product struct {
	gorm.Model
	Code  string `gorm:"type:varchar(16);uniqueIndex"`
	Price uint   `gorm:"type:tinyint;not null"`
}

func basic_crud(db *gorm.DB) {
	// Create Table
	db.AutoMigrate(&Product{}) // AutoMigrate 会自动创建表，如果表已存在，则不会创建

	// Show Table Schema
	columns, _ := db.Migrator().ColumnTypes(&Product{})
	for _, column := range columns {
		fmt.Printf("column: %s[%s]\n", column.Name(), column.DatabaseTypeName())
	}
	indexes, _ := db.Migrator().GetIndexes(&Product{})
	for _, index := range indexes {
		fmt.Printf("index: %s\n", index.Name())
	}

	// Insert
	db.Create(&Product{Code: "D42", Price: 100})

	// Select
	var product Product
	db.First(&product, 1)                 // find product with integer primary key
	db.First(&product, "code = ?", "D42") // find product with code D42

	// Update - update one field
	db.Model(&product).Update("Price", 200)
	// Update - update multiple fields
	db.Model(&product).Updates(Product{Price: 200, Code: "F42"}) // non-zero fields
	db.Model(&product).Updates(map[string]interface{}{"Price": 200, "Code": "F42"})

	// Delete - delete product
	db.Delete(&product, 1)

	// Drop Table
	db.Migrator().DropTable(&Product{})
}

func dry_run_crud(db *gorm.DB) {
	var stmt *gorm.Statement
	var product Product

	stmt = db.Session(&gorm.Session{DryRun: true}).Create(&Product{Code: "D42", Price: 100}).Statement
	fmt.Println(stmt.SQL.String(), stmt.Vars)
	stmt = db.Session(&gorm.Session{DryRun: true}).First(&Product{}, 1).Statement
	fmt.Println(stmt.SQL.String(), stmt.Vars)
	stmt = db.Session(&gorm.Session{DryRun: true}).First(&Product{}, "code = ?", "D42").Statement
	fmt.Println(stmt.SQL.String(), stmt.Vars)
	stmt = db.Session(&gorm.Session{DryRun: true}).Model(&product).Update("Price", 200).Statement
	fmt.Println(stmt.SQL.String(), stmt.Vars)
	stmt = db.Session(&gorm.Session{DryRun: true}).Model(&product).Updates(Product{Price: 200, Code: "F42"}).Statement
	fmt.Println(stmt.SQL.String(), stmt.Vars)
}

func main() {
	db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	basic_crud(db)
	fmt.Println("--------------------------------")
	dry_run_crud(db)
}
