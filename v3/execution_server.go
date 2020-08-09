package main

import (
	"fmt"
	"log"
	"net/http"
)

func liveness(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "Execution Server: live\n")
}

func headers(w http.ResponseWriter, req *http.Request) {

	for name, headers := range req.Header {
		for _, h := range headers {
			fmt.Fprintf(w, "%v: %v\n", name, h)
		}
	}
}

func handleRequests() {
	http.HandleFunc("/liveness", liveness)
	http.HandleFunc("/headers", headers)

	log.Fatal(http.ListenAndServe(":8090", nil))
}

func main() {
	handleRequests()
}