package db

import (
	"crypto/rand"
	"database/sql"
	"encoding/hex"
	"errors"
	"fmt"
	"time"

    _ "github.com/mattn/go-sqlite3"
)

const FILE = "users.db"
const TABLE = "Users"

type DataBase struct {
	*sql.DB
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


func (db *DataBase) GetPublicKey(id string) (string, error) {
	rows, _ := db.Query(fmt.Sprintf("SELECT publicKey FROM %s WHERE id = ?", TABLE), id)

	var publicKey string
	for rows.Next() {
		if err := rows.Scan(&publicKey); err != nil {
			return "", err
		}
	}

	if len(publicKey) > 0 {
		return publicKey, nil
	} else {
		return "", errors.New("wrong publicKey")
	}
}


func (db *DataBase) SaveUser(publicKey string) string {
	id, _ := randomHex(5)
	date := time.Now()

	statement, _ := db.Prepare(fmt.Sprintf("INSERT INTO %s VALUES (?, ?, ?)", TABLE))
	statement.Exec(id, publicKey, date)

	return id
}


func (db *DataBase) UpdateLastActivity(id string) {
	date := time.Now()

	statement, _ := db.Prepare(fmt.Sprintf("UPDATE %s SET last_activity = ? WHERE ID = ?", TABLE))
	statement.Exec(date, id)
}
