package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
	"github.com/gorilla/mux"
)

// Position - Representation of Single Stock
type Position struct {
	Ticker           string    `json:"ticker"`
	PurchasePrice    float32   `json:"purchase_price"`
	PurchaseQuantity int64     `json:"purchase_Quantity"`
	PurchaseDate     time.Time `json:"purchase_date"`
}

// Positions - Representation of Collection of Stocks (Portfolio)
var Positions []Position

func getPositions(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(Positions)
}

func liveness(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "Execution Server: Live\n")
}

func handleRequests() {

	fmt.Println("Server Started: ", time.Now(), "|| Listening on :8090", "|| Execution Server: Ready")

	myRouter := mux.NewRouter().StrictSlash(true)

	myRouter.HandleFunc("/", liveness).Methods("GET")
	myRouter.HandleFunc("/positions", getPositions).Methods("GET")

	log.Fatal(http.ListenAndServe(":8090", myRouter))
}

func main() {
	Positions = []Position{
		Position{
			Ticker: "AAPL", PurchasePrice: 200.50, PurchaseQuantity: 5, PurchaseDate: time.Now()
		},
		Position{
			Ticker: "F", PurchasePrice: 41.75, PurchaseQuantity: 3, PurchaseDate: time.Now().Add(time.Duration(100))
		},
	}

	handleRequests()
}
