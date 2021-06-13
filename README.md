<img src="https://raw.githubusercontent.com/PradyumnaKrishna/PradyumnaKrishna/master/logo.svg" alt="Logo" title="Logo" align="right" height="50" width="50"/>

# Enigma Protocol [![Build][Build-Badge]][Builds] [![Pages][Pages-Badge]][Pages]

Hello Friends, I built an end to end encrypted messenger using Flask, SocketIO, and Vue.js.


## Working

The Chat is encrypted using RSA encrytion that is a public key encryption or you can say asymmetric encryption. RSA gives two keys, public key and private key, public key is used to encrypt messages while private key is used to decrypt them.

I have used [Diffie–Hellman key exchange](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) to exchange the public keys of the users. These keys are used by user A to encrypt messages and send them to another user B and user B can decrypt them using his private key.

Socket.io is used to send and receive messages, these messages are encrypted and sent to the user having the private key to decrypt it.

I created some Flask API to store the information* of the users in a SQLite database and relogin as the user if page reloaded.

Finally Vue.js is used to perform client side encryption/decryption, send/receive message and login or connect to the user.

*Information contains `id`, `publicKey`, and `last_activity` of a user.


## Docs

Docs are coming soon on the website: https://protocol.onpy.in/#/docs.


## Development

Those who wants to develop or build the code then, just clone this repository using:

```bash
git clone https://github.com/PradyumnaKrishna/enigma-protocol.git
```

### Server (Python 3)
- Open up the server folder
- install the requirements
```bash
pip3 install -r requirements.txt
```
- OR build docker image
```bash
docker build -t protocol-server .
```

Supported Python Versions
- Python 3.7/3.8

### Client (Vue.js)
- Open up the client folder
- install the requirements
```bash
npm ci
```
- run the development server
```bash
npm run serve
```
- build the vue.js app
```bash
npm run build
```
- OR use docker to build
```bash
docker build -t protocol-client .
```

**NOTE**: To run the vue.js app you need to confiure an env variables, open `.env.sample` to see an sample environment file.

Supported Node.js Version
- I used current LTS version, that is node v14.17.0


## What next

I opened a project on this github repo, If possible I will commit and make additions to this repository as mentioned in the project.


[Build-Badge]:          https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/docker-build.yml/badge.svg

[Builds]:               https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/docker-build.yml

[Pages-Badge]:          https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/github-pages.yml/badge.svg

[Pages]:                https://protocol.onpy.in

