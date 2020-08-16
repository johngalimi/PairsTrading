package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

// Transaction - Representation of Single Buy/Sell Order
type Transaction struct {
	Ticker   string    `json:"ticker"`
	Price    float32   `json:"price"`
	Quantity int       `json:"quantity"`
	Date     time.Time `json:"date"`
}

// Transactions - Representation of Collection of Transactions
var Transactions []Transaction

// Position - Representation of Position in Portfolio
type Position struct {
	Ticker   string `json:"ticker"`
	Quantity int    `json:"quantity"`
}

func getTransactions(w http.ResponseWriter, r *http.Request) {
	// method to get list of transactions
	json.NewEncoder(w).Encode(Transactions)
}

// we should have a handler that checks acct balance / validity of transaction first
func executeTransaction(w http.ResponseWriter, r *http.Request) {
	// method to execute transaction
	// BUY --> curl -X POST -H 'Content-Type: application/json' -d "{\"ticker\":\"FB\", \"price\":182.76, \"quantity\":15}" localhost:8090/transaction
	// SELL --> curl -X POST -H 'Content-Type: application/json' -d "{\"ticker\":\"FB\", \"price\":181.76, \"quantity\":-13}" localhost:8090/transaction
	var transaction Transaction

	json.NewDecoder(r.Body).Decode(&transaction)

	Transactions = append(Transactions, transaction)

	json.NewEncoder(w).Encode(transaction)
}

func constructPortfolio() map[string]int {
	// method to construct portfolio by aggregating across transactions

	portfolio := make(map[string]int)

	for _, transaction := range Transactions {
		portfolio[transaction.Ticker] += transaction.Quantity
	}

	return portfolio
}

func getPositions(w http.ResponseWriter, r *http.Request) {
	// method to construct portfolio and serve it up

	var Positions []Position

	portfolio := constructPortfolio()

	for ticker, quantity := range portfolio {
		Positions = append(Positions, Position{Ticker: ticker, Quantity: quantity})
	}

	json.NewEncoder(w).Encode(Positions)
}

func liveness(w http.ResponseWriter, req *http.Request) {
	// method to indicate that service is live
	fmt.Fprintf(w, "Execution Server: Live\n")
}

func handleRequests() {
	// method to set-up router and endpoints to serve up

	var port string = ":8090"

	fmt.Println("Server Started: ", time.Now(), "|| Listening on", port, "|| Execution Server: Ready")

	myRouter := mux.NewRouter().StrictSlash(true)

	myRouter.HandleFunc("/", liveness).Methods("GET")
	myRouter.HandleFunc("/transactions", getTransactions).Methods("GET")
	myRouter.HandleFunc("/transaction", executeTransaction).Methods("POST")
	myRouter.HandleFunc("/positions", getPositions).Methods("GET")

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
		Transaction{
			Ticker:   "F",
			Price:    41.75,
			Quantity: -2,
			Date:     time.Now().Add(time.Duration(200)),
		},
	}

	handleRequests()
}
