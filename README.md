<img src="https://raw.githubusercontent.com/PradyumnaKrishna/PradyumnaKrishna/master/logo.svg" alt="Logo" title="Logo" align="right" height="50" width="50"/>

# Enigma Protocol [![Build][Build-Badge]][Builds] [![Pages][Pages-Badge]][Pages]

Hello Friends, I am trying to build an end to end encrypted messenger using Flask, SocketIO, and Vue.js. So, Here is my roadmap to achieve it.


## Initial Roadmap 

**Moved to [Projects](https://github.com/PradyumnaKrishna/enigma-protocol/projects/2).**


## Logic

Here is a logic behind this system, RSA is a cryptographic algorithm that gives you two pair of keys: public and private.

Public Key is used to encrypt messages while private key is used to decrypt them, no one can decrypt any encrypted message without private key.

Thats why I chose to exchange those public keys, which means anyone can encrypt and send encrypted messaged to the user but they can't decrypt them.

The logic behind database storing facility is simple, Database is used to store messages with session, user and timestamp.

If by chance anyone wants to restore that session, he can by retrieving messages from database.

~~But here is a small drawback of end-to-end encryption. The user can't decrypt their messages, those messages are stored to the database but the user doesn't have the key to decrypt them.~~
Recently, I changed the method and stored the messages on client side also, which is used to retreive messages.

**`...`**


## Development

The Development is in progress, so those who wants to develop with me just clone this repository using:

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

Supported Node.js Version
- I used current LTS version, that is node v14.17.0

[Build-Badge]:          https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/docker-build.yml/badge.svg

[Builds]:               https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/docker-build.yml

[Pages-Badge]:          https://github.com/PradyumnaKrishna/Enigma-Protocol/actions/workflows/github-pages.yml/badge.svg

[Pages]:                https://protocol.onpy.in

