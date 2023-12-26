package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"

	socketio "github.com/googollee/go-socket.io"
	"github.com/googollee/go-socket.io/engineio"
	"github.com/googollee/go-socket.io/engineio/transport"
	"github.com/googollee/go-socket.io/engineio/transport/polling"
	"github.com/googollee/go-socket.io/engineio/transport/websocket"

	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"

	"main/db"
)


var allowOriginFunc = func(r *http.Request) bool {
	return true
}


var database = &db.DataBase{DB: db.NewConn()}
var myRouter = mux.NewRouter().StrictSlash(true)
var server = socketio.NewServer(&engineio.Options{
	Transports: []transport.Transport{
		&polling.Transport{
			CheckOrigin: allowOriginFunc,
		},
		&websocket.Transport{
			CheckOrigin: allowOriginFunc,
		},
	},
})


type Response struct {
	Status bool `json:"status"`
	User string `json:"user,omitempty"`
	To string `json:"to,omitempty"`
	PublicKey string `json:"publicKey,omitempty"`
}

type Message struct {
	User string `json:"user"`
	Text string `json:"message,omitempty"`
	To string `json:"to,omitempty"`
}


func JSONResponse(w http.ResponseWriter, code int, output interface{}) {
	// Convert our interface to JSON
	response, err := json.Marshal(output)
	if err != nil {
		log.Printf("Error marshalling JSON response: %v\n", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	// Set the content type to json for browsers
	w.Header().Set("Content-Type", "application/json")
	// Our response code
	w.WriteHeader(code)

	w.Write(response)
}


func homePage(w http.ResponseWriter, r *http.Request) {
	log.Println("/ endpoint reached")
	w.Write([]byte("ok"))
}


func login(w http.ResponseWriter, r *http.Request) {
	log.Println("/login endpoint reached")

	vars := mux.Vars(r)
	id := database.SaveUser(vars["publicKey"])

	response := Response{
		Status: true,
		User: id,
	}

	JSONResponse(w, http.StatusOK , response)
}


func connect(w http.ResponseWriter, r *http.Request) {
	log.Println("/connect endpoint reached")

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

	JSONResponse(w, http.StatusOK , response)
}


func InitializeSockets() {
	server.OnConnect("/", func(s socketio.Conn) error {
		s.SetContext("")
		log.Println("connected:", s.ID())
		return nil
	})

	server.OnEvent("/", "join_room", func(s socketio.Conn, m Message) {
		s.Join(m.User)
		server.BroadcastToRoom("/", m.User, "room_announcements", "Join Room Callback")
	})

	server.OnEvent("/", "send_message", func(s socketio.Conn, m Message) {
		log.Println(m.To)
		server.BroadcastToRoom("/", m.To, "receive_message", m)
	})
}


func InitializeRoutes() {
	myRouter.HandleFunc("/", homePage)
	myRouter.HandleFunc("/login/{publicKey}", login)
	myRouter.HandleFunc("/connect/{id}", connect)

	cors := handlers.CORS(
		handlers.AllowedHeaders([]string{"content-type"}),
		handlers.AllowedOrigins([]string{"*"}),
		handlers.AllowCredentials(),
	)

	myRouter.Use(cors)
}


func Init() {
	go func() {
		if err := server.Serve(); err != nil {
			log.Fatalf("socketio listen error: %s\n", err)
		}
	}()
	defer func() {
		if err := server.Close(); err != nil {
			log.Printf("Error closing server: %s\n", err)
		}
	}()

	http.Handle("/socket.io/", server)
	http.Handle("/", myRouter)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Println("Serving at localhost:" + port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}


func main() {
	InitializeSockets()
	InitializeRoutes()
	Init()
}
