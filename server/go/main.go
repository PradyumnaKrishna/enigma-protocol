package main

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func randomHex(n int) (string, error) {
	bytes := make([]byte, n)
	if _, err := rand.Read(bytes); err != nil {
	  return "", err
	}
	return hex.EncodeToString(bytes), nil
}


type newResponse struct {
	User string `json:"user"`
}


type connectResponse struct {
	Status bool `json:"status"`
	To string `json:"to,omitempty"`
	PublicKey string `json:"publicKey,omitempty"`
}


func JSONResponse(w http.ResponseWriter, code int, output interface{}) {
	// Convert our interface to JSON
	response, _ := json.Marshal(output)
	// Set the content type to json for browsers
	w.Header().Set("Content-Type", "application/json")
	// Our response code
	w.WriteHeader(code)

	w.Write(response)
}


func homePage(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "ok")
    fmt.Println("Endpoint Hit: homePage")
}


func new(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
    publicKey := vars["publicKey"]

	log.Println(publicKey)

	hex, _ := randomHex(5)

	response := newResponse{
		User: hex,
	}

	JSONResponse(w, 200, response)
}


func handleRequests() {
    myRouter := mux.NewRouter()
    myRouter.HandleFunc("/", homePage)
    myRouter.HandleFunc("/login/{publicKey}", new)
    log.Fatal(http.ListenAndServe(":8000", myRouter))
}

func main() {
	handleRequests()
}
