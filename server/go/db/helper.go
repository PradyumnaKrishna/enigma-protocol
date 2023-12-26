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


func NewConn() (*sql.DB, error) {
	database, err := sql.Open("sqlite3", FILE)
	if err != nil {
		return nil, err
	}

	statement, err := database.Prepare(fmt.Sprintf("CREATE TABLE IF NOT EXISTS %s (id TEXT PRIMARY KEY, publicKey TEXT, last_activity DATE)", TABLE))
	if err != nil {
		return nil, err
	}
	_, err = statement.Exec()
	if err != nil {
		return nil, err
	}

	return database, nil
}


func (db *DataBase) GetPublicKey(id string) (string, error) {
	var publicKey string
	err := db.QueryRow(fmt.Sprintf("SELECT publicKey FROM %s WHERE id = ?", TABLE), id).Scan(&publicKey)
	if err != nil {
		return "", err
	}

	if len(publicKey) > 0 {
		return publicKey, nil
	}
	return "", errors.New("wrong publicKey")
}


func (db *DataBase) SaveUser(publicKey string) (string, error) {
	id, err := randomHex(5)
	if err != nil {
		return "", err
	}

	date := time.Now()
	statement, err := db.Prepare(fmt.Sprintf("INSERT INTO %s VALUES (?, ?, ?)", TABLE))
	if err != nil {
		return "", err
	}
	_, err = statement.Exec(id, publicKey, date)
	if err != nil {
		return "", err
	}

	return id, nil
}


func (db *DataBase) UpdateLastActivity(id string) {
	date := time.Now()

	statement, _ := db.Prepare(fmt.Sprintf("UPDATE %s SET last_activity = ? WHERE ID = ?", TABLE))
	statement.Exec(date, id)
}
