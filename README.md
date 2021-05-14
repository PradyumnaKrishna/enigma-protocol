
# Title

Hello Friends, I am trying to build an end to end encrypted messenger using Flask, SocketIO, and Vue.js. So, Here is my roadmap to achieve it.


## Initial Roadmap 

**Moved to [Projects](https://github.com/PradyumnaKrishna/enigma-protocol/projects/2).**


## Logic

Here is a logic behind this system, RSA is a cryptographic algorithm that gives you two pair of keys: public and private.

Public Key is used to encrypt messages while private key is used to decrypt them, no one can decrypt any encrypted message without private key.

Thats why I chose to exchange those public keys, which means anyone can encrypt and send encrypted messaged to the user but they can't decrypt them.

The logic behind database storing facility is simple, Database is used to store messages with session, user and timestamp.

If by chance anyone wants to restore that session, he can by retrieving messages from database.

But here is a small drawback of end-to-end encryption. The user can't decrypt their messages, those messages are stored to the database but the user doesn't have the key to decrypt them.

**`...`**


## Development

The Development is in progress, so those who wants to develop with me just clone this repository using:

```bash
git clone <repository-url>
```

install the requirements

```bash
pip3 install -r requirements.txt

npm install
```

**Prerequisite**
- [ ] python 3.7/3.8
- [ ] node.js
