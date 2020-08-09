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
	PurchaseQuantity int64     `json:"purchase_quantity"`
	PurchaseDate     time.Time `json:"purchase_date"`
}

// Positions - Representation of Collection of Stocks (Portfolio)
var Positions []Position

func getPositions(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(Positions)
}

func enterPosition(w http.ResponseWriter, r *http.Request) {
	// curl -X POST -H 'Content-Type: application/json' -d "{\"ticker\":\"FB\", \"purchase_price\":182.76, \"purchase_quantity\":15}" localhost:8090/position
	var position Position

	json.NewDecoder(r.Body).Decode(&position)

	Positions = append(Positions, position)

	json.NewEncoder(w).Encode(position)

	cleanPortfolio()
}

func cleanPortfolio() {
	for _, position := range Positions {
		fmt.Println(position.Ticker)
	}
}

func liveness(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "Execution Server: Live\n")
}

func handleRequests() {

	var port string = ":8090"

	fmt.Println("Server Started: ", time.Now(), "|| Listening on", port, "|| Execution Server: Ready")

	myRouter := mux.NewRouter().StrictSlash(true)

	myRouter.HandleFunc("/", liveness).Methods("GET")
	myRouter.HandleFunc("/positions", getPositions).Methods("GET")
	myRouter.HandleFunc("/position", enterPosition).Methods("POST")

	log.Fatal(http.ListenAndServe(port, myRouter))
}

func main() {
	Positions = []Position{
		Position{
			Ticker:           "AAPL",
			PurchasePrice:    200.50,
			PurchaseQuantity: 5,
			PurchaseDate:     time.Now(),
		},
		Position{
			Ticker:           "F",
			PurchasePrice:    41.75,
			PurchaseQuantity: 3,
			PurchaseDate:     time.Now().Add(time.Duration(100)),
		},
	}

	handleRequests()
}
