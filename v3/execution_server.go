package main

import (
	"fmt"
	"log"
	"time"
	"net/http"
	// "encoding/json"
	"github.com/gorilla/mux"
)

type Position struct {
	ticker string 
	purchasePrice float32
	purchaseQuantity int64
	purchaseDatetime time.Time
}


func liveness(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "Execution Server: Live\n")
}

func headers(w http.ResponseWriter, req *http.Request) {

	for name, headers := range req.Header {
		for _, h := range headers {
			fmt.Fprintf(w, "%v: %v\n", name, h)
		}
	}
}

func handleRequests() {

	fmt.Println(time.Now(), "Execution Server: Ready")

	myRouter := mux.NewRouter().StrictSlash(true)

	myRouter.HandleFunc("/liveness", liveness)
	myRouter.HandleFunc("/headers", headers)

	log.Fatal(http.ListenAndServe(":8090", myRouter))
}

func main() {
	handleRequests()
}