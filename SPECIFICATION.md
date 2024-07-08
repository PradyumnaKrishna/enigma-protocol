# Enigma Protocol Specification

**Date**: July 8, 2024  
**Version**: 0.3.0 (Draft)

## Overview

The specification describes the protocol and algorithm for secure key (public key) exchange and message transmission between two users. The process is centralized, requiring a centralized node or Enigma Server.

Encryption and decryption of messages are not covered in this document. For details on message encryption and decryption, refer to the [Protocol](PROTOCOL.md).

## Enigma Server

The Enigma Server functions as a centralized server responsible for storing users' public keys and facilitating message transmission between them. The server must perform the following tasks:

1. Store users' public keys.
2. Transmit messages between users.
3. Facilitate key exchange between users.

The server must implement required REST APIs and WebSockets, and it must handle multiple users and connections concurrently.

### REST API Endpoints

The server must provide the following REST APIs:

#### User Login

`GET /login/{publicKey}`

- **Description**: Stores the user's public key and assigns a userId.
- **Request**: 
  - `publicKey`: The public key of the user.
- **Response**: A JSON object containing:
  - `userId`: The unique identifier of the user.
- **Status Codes**:
  - `200`: Successful login.

#### Get Public Key

`GET /connect/{userId}`

- **Description**: Retrieves the public key of the specified user.
- **Request**: 
  - `userId`: The unique identifier of the requested user.
- **Response**: A JSON object containing:
  - `userId`: The unique identifier of the requested user.
  - `publicKey`: The public key of the requested user.
- **Status Codes**:
  - `200`: Public key retrieved successfully.
  - `404`: Requested user not found.

### WebSockets

The server must provide a WebSocket endpoint for users to connect and transmit messages.

`WebSocket /connect/{userId}`

- **Description**: Connect to the server to receive messages.
- **Request**: 
  - `userId`: The unique identifier of the user.
- **Response**: If the user does not exist, the connection is closed with a JSON response containing:
  - `error`: Error message.

#### Message Transmission

The server must transmit messages between connected users and store pending messages in Redis or similar storage.

The JSON structure used to transmit messages is as follows:

```json
{
  "from": "<userId>",
  "to": "<userId>",
  "payload": "<encryptedMessage>"
}
```

- `from`: Unique identifier of the sender.
- `to`: Unique identifier of the receiver.
- `payload`: Encrypted message.

## Operation

### Key Exchange

Key exchange uses the Diffie-Hellman key exchange algorithm to exchange users' public keys. More information about the algorithm can be found [here](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange).

The key exchange process involves the following steps:

- Alice and Bob generate their public and private keys.
- Alice and Bob log their public keys on the server using the `/login` endpoint and obtain their respective userIds.
- Alice requests Bob's public key using the `/connect` endpoint.


### Message Transmission

1. Alice connects to the server using the `/connect` WebSocket endpoint.
2. Alice sends a message to Bob using the following JSON object:
   ```json
   {
     "from": "<userId>",
     "to": "<userId>",
     "payload": "<encryptedMessage>"
   }
   ```
3. If Bob is connected, the server transmits the message to Bob via the WebSocket connection.
4. If Bob is not connected, the server stores the message in Redis or similar storage and delivers it when Bob reconnects.
5. If Bob cannot be found, the server notifies Alice with an error message.
