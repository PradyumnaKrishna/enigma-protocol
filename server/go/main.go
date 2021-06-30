package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"main/db"
)


var database = &db.DataBase{DB: db.NewConn()}


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


func login(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)

	id := database.SaveUser(vars["publicKey"])

	response := Response{
		Status: true,
		User: id,
	}

	JSONResponse(w, 200, response)
}


func connect(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	publicKey, err := database.GetPublicKey(id)

	response := Response{Status: false}
	if err == nil {
		response = Response{
			Status: true,
			To: id,
			PublicKey: publicKey,
		}
	}

	JSONResponse(w, 200, response)
}


func handleRequests() {
    myRouter := mux.NewRouter().StrictSlash(true)
    myRouter.HandleFunc("/", homePage)
    myRouter.HandleFunc("/login/{publicKey}", login)
    myRouter.HandleFunc("/connect/{id}", connect)
    log.Fatal(http.ListenAndServe(":8000", myRouter))
}


func main() {
	handleRequests()
}
