package main

import (
	"APItest/controllers"
	"APItest/database"
	"APItest/models"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	database.Connect()
	database.DB.AutoMigrate(&models.Book{})

	router.GET("/books", controllers.GetBooks)
	router.POST("/books", controllers.CreateBook)
	router.GET("/quote/:id", controllers.GetQuote) // external API
	router.PUT("/checkout/:id", controllers.CheckoutBook)
	router.PUT("/return/:id", controllers.ReturnBook)
	router.DELETE("/books/:id", controllers.DeleteBook)

	router.Run("localhost:8080")
}
