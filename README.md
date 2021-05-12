
# Title

Hello Friends, I am trying to build an end to end encrypted messenger using Flask, SocketIO, and Vue.js. So, Here is my roadmap to achieve it.


## Initial Roadmap 

### Build a Person to Person Chat messenger

- [ ] Generate Hash for each user, whoever opened the client using flask.

- [ ] Store that Hash into database and on client session.

- [ ] Connect other user using Hash.

- [ ] Create a 2 person session on frontend.

### Add encryption to those messages

- [ ] Create 2 SocketIO, one for send and another for receive.

- [ ] Encrypt those messages using node-forge (node.js's api crypto not working with vue.js currently).

- [ ] While Creating session exchange the public keys of the users.

- [ ] Encrypt using publicKey, decrypt using privateKey and these keys are going to store in frontend session.

-  **NOTE: If privateKey or user hash removed from the session then no one can restore those messages.**

### DataBase Storing Facility

- [ ] Store every message to the database (with session id that is going to be another Hash) while send and receive messages.

- [ ] Session is removed after 15 min of last activity (initially).

- [ ] One button deletion of encrypted messages and user from database.

-  **NOTE: Only Received Messages can be decrypted, You can't decrypt sent messages because you have don't have privateKey for sent one.**

### **`...`**


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
