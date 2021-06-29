package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

    "main/db"
	"github.com/gorilla/mux"
)


var conn = db.Conn{
	DB: db.NewConn(),
}

type Response struct {
	Status bool `json:"status"`
	User string `json:"user,omitempty"`
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

	log.Println(vars["publicKey"])

	response := Response{
		Status: true,
		User: "hex",
	}

	JSONResponse(w, 200, response)
}

func connect(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)

	log.Println(vars["id"])

	response := Response{
		Status: true,
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
