package db

import (
	"crypto/rand"
    "database/sql"
	"encoding/hex"
	"errors"
	"fmt"
    // "log"
	"time"

    _ "github.com/mattn/go-sqlite3"
)

const FILE = "users.db"
const TABLE = "Users"

type Conn struct {
	DB *sql.DB
}


func randomHex(n int) (string, error) {
	bytes := make([]byte, n)
	if _, err := rand.Read(bytes); err != nil {
	  return "", err
	}
	return hex.EncodeToString(bytes), nil
}


func NewConn() *sql.DB {
	database, _ := sql.Open("sqlite3", FILE)

	statement, _ := database.Prepare(fmt.Sprintf("CREATE TABLE IF NOT EXISTS %s (id TEXT PRIMARY KEY, publicKey TEXT, last_activity DATE)", TABLE))
	statement.Exec()	
	
	return database
}


func (conn Conn) GetPublicKey(id string) (string, error) {
	rows, _ := conn.DB.Query(fmt.Sprintf("SELECT publicKey FROM %s WHERE id = ?", TABLE), id)

	var publicKey string
	for rows.Next() {
		if err := rows.Scan(&publicKey); err != nil {
			return "", err
		}
	}

	if len(publicKey) > 0 {
		return publicKey, nil
	} else {
		return "", errors.New("Wrong publicKey")
	}
}

func (conn Conn) SaveUser(publicKey string) string {
	id, _ := randomHex(5)
	date := time.Now()


	statement, _ := conn.DB.Prepare(fmt.Sprintf("INSERT INTO %s VALUES (?, ?, ?)", TABLE))
	statement.Exec(id, publicKey, date)

	return id
}
