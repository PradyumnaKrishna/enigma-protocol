<img src="https://raw.githubusercontent.com/PradyumnaKrishna/PradyumnaKrishna/master/logo.svg" alt="Logo" title="Logo" align="right" height="50" width="50"/>

# Enigma Protocol [![Python Server][Python-Badge]][Python] [![Github Pages][Pages-Badge]][Pages]

Hello Friends, I built an end to end encrypted messenger using Flask, SocketIO, and Vue.js.


## Working

The Chat is encrypted using RSA encryption that is a public key encryption or you can say asymmetric encryption. RSA gives two keys, public key and private key, public key is used to encrypt messages while private key is used to decrypt them.

I have used [Diffie–Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) to exchange the public keys of the users. These keys are used by user A to encrypt messages and send them to another user B and user B can decrypt them using his private key.

Socket.io is used to send and receive messages, these messages are encrypted and sent to the user having the private key to decrypt it.

I created some Flask API to store the information* of the users in a SQLite database and relogin as the user if page reloaded.

Finally Vue.js is used to perform client side encryption/decryption, send/receive message and login or connect to the user.

*Information contains `id`, `publicKey`, and `last_activity` of a user.


## Development

Those who wants to develop or build the code then, just clone this repository using:

```bash
git clone https://github.com/PradyumnaKrishna/enigma-protocol.git
```

### Server (Python 3)
- Install Dependencies
```bash
pip3 install -r requirements.txt
```
- Run the Server
```bash
python main.py
```

Supported Python Versions
- Python 3.7/3.8


### Server (Golang)
This is on hold because go-socket.io doesn't support newer versions of client-socket.io.


### Client (Vue.js)
- Install Dependencies
```bash
npm ci
```
- Run the development client
```bash
npm run serve
```

**NOTE**: To run the vue.js app you need to confiure an env variables, open `.env.sample` to see an sample environment file.

Supported Node.js Version
- Current LTS version (14) or newer

## What next

I will create Issues and try to fix them.


[Python-Badge]:          https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/python_build.yml/badge.svg

[Python]:                https://ghcr.io/PradyumnaKrishna/enigma-protocol/python-server

[Pages-Badge]:           https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/client_build.yml/badge.svg

[Pages]:                 https://protocol.onpy.in

