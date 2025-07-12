package database

import (
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
)

var DB *gorm.DB

func Connect() {
	dsn := "host=localhost user=USER password=PASSWORD dbname=API port=5432 sslmode=disable"

	db, err := gorm.Open(postgres.New(postgres.Config{
		DSN:                  dsn,
		PreferSimpleProtocol: true,
	}), &gorm.Config{})

	if err != nil {
		log.Fatal("Error connecting db :", err)
	}

	DB = db
}
