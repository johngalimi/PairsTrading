package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

// Transaction - Representation of Single Buy/Sell
type Transaction struct {
	Ticker   string    `json:"ticker"`
	Price    float32   `json:"price"`
	Quantity int64     `json:"quantity"`
	Date     time.Time `json:"date"`
}

// Transactions - Representation of Collection of Transactions (Portfolio)
var Transactions []Transaction

func getTransactions(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(Transactions)
}

func executeTransaction(w http.ResponseWriter, r *http.Request) {
	// curl -X POST -H 'Content-Type: application/json' -d "{\"ticker\":\"FB\", \"price\":182.76, \"quantity\":15}" localhost:8090/position
	var transaction Transaction

	json.NewDecoder(r.Body).Decode(&transaction)

	Transactions = append(Transactions, transaction)

	json.NewEncoder(w).Encode(transaction)

	cleanPortfolio()
}

func cleanPortfolio() {
	for _, transaction := range Transactions {
		fmt.Println(transaction.Ticker)
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
	myRouter.HandleFunc("/transactions", getTransactions).Methods("GET")
	myRouter.HandleFunc("/transaction", executeTransaction).Methods("POST")

	log.Fatal(http.ListenAndServe(port, myRouter))
}

func main() {
	Transactions = []Transaction{
		Transaction{
			Ticker:   "AAPL",
			Price:    200.50,
			Quantity: 5,
			Date:     time.Now(),
		},
		Transaction{
			Ticker:   "F",
			Price:    41.75,
			Quantity: 3,
			Date:     time.Now().Add(time.Duration(100)),
		},
	}

	handleRequests()
}
