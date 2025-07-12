package models

type Book struct {
	ID       uint   `json:"id" gorm:"primaryKey"`
	Title    string `json:"title"`
	Author   string `json:"author"`
	Quantity int    `json:"quantity"`
}

type Quote struct {
	ID           string   `json:"_id"`
	Content      string   `json:"content"`
	Author       string   `json:"author"`
	Tags         []string `json:"tags"`
	AuthorSlug   string   `json:"authorSlug"`
	Length       int      `json:"length"`
	DateAdded    string   `json:"dateAdded"`
	DateModified string   `json:"dateModified"`
}

type QuoteResponse struct {
	Count         int     `json:"count"`
	TotalCount    int     `json:"totalCount"`
	Page          int     `json:"page"`
	TotalPages    int     `json:"totalPages"`
	LastItemIndex int     `json:"lastItemIndex"`
	Results       []Quote `json:"results"`
}
