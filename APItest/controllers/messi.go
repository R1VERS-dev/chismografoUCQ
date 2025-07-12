package controllers

import (
	"APItest/database"
	"APItest/models"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"net/http"
	"net/url"
)

func GetBooks(c *gin.Context) {
	var books []models.Book
	result := database.DB.Find(&books)

	if result.Error != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
		return
	}

	c.IndentedJSON(http.StatusOK, books)
}

func CreateBook(c *gin.Context) {
	var newBook models.Book

	if err := c.ShouldBindJSON(&newBook); err != nil {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result := database.DB.Create(&newBook)
	if result.Error != nil {
		c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
		return
	}

	c.IndentedJSON(http.StatusCreated, newBook)
}

func GetQuote(c *gin.Context) {
	id := c.Param("id")
	var book models.Book

	result := database.DB.First(&book, id)
	if result.Error != nil {
		c.IndentedJSON(http.StatusNotFound, gin.H{"error": "Book not found"})
		return
	}

	baseURL := "http://api.quotable.io/quotes"
	params := url.Values{}
	params.Add("author", book.Author)
	params.Add("limit", "1")
	fullURL := fmt.Sprintf("%s?%s", baseURL, params.Encode())

	resp, err := http.Get(fullURL)
	if err != nil {
		c.IndentedJSON(http.StatusServiceUnavailable, gin.H{"error": "Error connecting external API"})
		return
	}

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": "Error reading response body"})
		return
	}

	var quote models.QuoteResponse
	err = json.Unmarshal(body, &quote)

	if err != nil {
		c.IndentedJSON(http.StatusInternalServerError, gin.H{"error": "Skill Issue"})
		return
	}

	c.IndentedJSON(http.StatusOK, gin.H{"quote": quote.Results[0].Content, "author": quote.Results[0].Author})

}

func CheckoutBook(c *gin.Context) {
	id := c.Param("id")
	var book models.Book

	result := database.DB.First(&book, id)
	if result.Error != nil {
		c.IndentedJSON(http.StatusNotFound, gin.H{"error": "Book not found"})
		return
	}

	if book.Quantity <= 0 {
		c.IndentedJSON(http.StatusBadRequest, gin.H{"error": "No copies available for checkout"})
		return
	}

	book.Quantity--
	database.DB.Save(&book)

	c.IndentedJSON(http.StatusOK, gin.H{"message": "Book checked out successfully", "remaining_quantity": book.Quantity})

}

func ReturnBook(c *gin.Context) {
	id := c.Param("id")
	var book models.Book

	result := database.DB.First(&book, id)
	if result.Error != nil {
		c.IndentedJSON(http.StatusNotFound, gin.H{"error": "Book not found"})
		return
	}

	book.Quantity++
	database.DB.Save(&book)

	c.IndentedJSON(http.StatusOK, gin.H{"message": "Book returned successfully", "new_quantity": book.Quantity})
}

func DeleteBook(c *gin.Context) {
	id := c.Param("id")
	var book models.Book

	result := database.DB.First(&book, id)
	if result.Error != nil {
		c.IndentedJSON(http.StatusNotFound, gin.H{"error": "Book not found"})
		return
	}

	database.DB.Delete(&book)

	c.IndentedJSON(http.StatusOK, gin.H{"message": "Book deleted successfully"})
}
