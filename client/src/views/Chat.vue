<template>
  <clip-loader v-if="loading"></clip-loader>
  <div v-else>
    <div class="d-flex justify-content-center">
      <div class="row justify-content-center h-75 w-100">
        <div class="col-md-4 col-xl-3 chat">
          <div class="card mb-sm-3 mb-md-0 h-100 contacts_card">
            <div class="card-header text-light">
              <ToastMessage :toastmsg="toastmsg" :toastType="toastType" />
              <UserInfo 
                :user="user" 
                @requestCopy="copy" 
                @joinRoom="join_room" 
              />
            </div>
            <div class="card-body contacts_body">
              <ChatListHeader :users="users" :activeUser="to" @switch="switchTo" />
            </div>
            <div class="card-footer"></div>
          </div>
        </div>
        <div class="col-md-8 col-xl-6 chat h-100">
          <div class="card">
            <div class="card-header">
              <div class="d-flex">
                <p class="text-b">
                  <strong>{{ to }}</strong>
                </p>
              </div>
            </div>
            <div ref="messages" class="card-body msg_card_body">
              <div v-if="!to">
                <img src="../assets/logo.png" />
                <p style="color: #42b983">
                  <strong>Protocol Initiated</strong>
                </p>
              </div>
              <div v-else v-for="item in messages">
                <div
                  v-if="item.user === 'self'"
                  class="d-flex justify-content-end mb-4"
                >
                  <div class="msg_container color-b text-b">
                    {{ item.message }}
                  </div>
                </div>
                <div v-else class="d-flex justify-content-start mb-4">
                  <div class="msg_container color-a text-a">
                    {{ item.message }}
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <form v-if="to && !isMessageFormDisabled" v-on:submit.prevent="onSubmit" class="form">
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control etrans"
                    v-model="message"
                    placeholder="Message"
                  />
                  <div class="input-group-append">
                    <button
                      v-bind:disabled="!message"
                      class="btn btn-dark"
                      style="color: #78e08f"
                      @click="send"
                    >
                      <strong>Send</strong>
                    </button>
                  </div>
                </div>
              </form>
              <p v-if="isMessageFormDisabled" style="color: #6c757d; font-weight: bold;">
              {{ inactiveUserMessage }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ToastMessage from "../components/ToastMessage.vue";
import UserInfo from "../components/UserInfo.vue";
import io from "socket.io-client";
import ClipLoader from "../assets/ClipLoader";
import { encryptMessage, decryptMessage } from "../utils/crypto";
import { Buffer } from "buffer";
import ChatListHeader from "../components/ChatListHeader.vue";

URL = process.env.VUE_APP_APIURL;

const forge = require("node-forge");
const fetch = require("node-fetch");
const socket = io.connect(URL);

export default {
  name: "Home",
  components: {
    UserInfo,
    ClipLoader,
    ChatListHeader,
    ToastMessage
  },
  data() {
    return {
      isMessageFormDisabled: false,
      inactiveUserMessage: '',
      loading: true,
      messages: [],
      message: "",
      users: [],
      user: null,
      toastmsg: "",
      toastType: "",
      to: null,
      room: null,
    };
  },
  methods: {
    copy: async function (text) {
      // finction to copy text to clipboard
      await navigator.clipboard.writeText(text);
      this.toastmsg = "Text Copied";
      this.toastType = "success";

      setTimeout(() => {
        this.toastmsg = "";
        this.toastType = "";
      }, 2000);
    },

    login: async function () {
      // login function used to restore session using cookie
      const publicKey = this.keypair.publicKey;
      if (this.$cookies.isKey("user")) {
        const user = this.$cookies.get("user");
        const response = await fetch(`${URL}/connect/${user}`);
        const json = await response.json();

        if (json.status) {
          this.user = user;
        } else {
          const response = await fetch(`${URL}/login/${publicKey}`);
          const json = await response.json();
          this.user = json.user;
          this.$cookies.set("user", this.user);
        }
      } else {
        const response = await fetch(`${URL}/login/${publicKey}`);
        const json = await response.json();
        this.user = json.user;
        this.$cookies.set("user", this.user);
      }
    },

    connect: async function (user) {
      // function to set publicKey of user and return status
      const response = await fetch(`${URL}/connect/${user}`);
      const json = await response.json();

      if (json.status) {
        this.$cookies.set(user, json.publicKey);
        return true;
      }
      return false;
    },

    retrieve: function (value) {
      // function retrieve messages from localStorage
      if (localStorage.getItem(value)) {
        try {
          this.messages = JSON.parse(localStorage.getItem(value));
        } catch (e) {
          localStorage.removeItem(value);
        }
      } else {
        this.messages = [];
      }
    },

    join_room: async function (user) {
      // make connection with other user
      const response = await this.connect(user);
      if (user !== this.user && response) {
        this.rearrange(user);
        this.switchTo(user);
      } else {
        this.toastmsg = "Wrong user";
        this.toastType = "error";

        setTimeout(() => {
          this.toastmsg = "";
          this.toastType = "";
        }, 2000);
      }
    },

    switchTo: async function (id) {
      // switch to the user select
      this.to = id;
      await this.retrieve(id);
      
      let publicKey = this.$cookies.get(id);;
      if (!publicKey || typeof publicKey !== 'string') {
        await this.connect(id);
        publicKey = this.$cookies.get(id);
        if (!publicKey || typeof publicKey !== 'string') {
          this.isMessageFormDisabled = true;
          this.inactiveUserMessage = "User is inactive";
          return
        }
      }

      this.isMessageFormDisabled = false;
      this.inactiveUserMessage = '';
      this[id] = Buffer.from(publicKey, "base64").toString();
      this.publicKey = forge.pki.publicKeyFromPem(this[id]);

      const container = this.$refs.messages;
      container.scrollTop = container.scrollHeight;
    },

    send: async function () {
      const message = encryptMessage(this.message, this.publicKey);

      socket.emit("send_message", {
        user: this.user,
        to: this.to,
        message: message,
      });

      await this.messages.push({ user: "self", message: this.message });
      this.setMessages(this.to, JSON.stringify(this.messages));
      this.rearrange(this.to);
      this.message = "";
    },

    setMessages: function (user, parsed) {
      // autoscroll to the bottom of container
      localStorage.setItem(user, parsed);

      const container = this.$refs.messages;
      container.scrollTop = container.scrollHeight;
    },

    rearrange: function (user) {
      // rearrange user
      const users = this.users.slice();
      users.unshift(user);

      this.users = [...new Set(users)];
      const parsed = JSON.stringify(this.users);
      localStorage.setItem("users", parsed);
    },

    load: async function () {
      this.loading = true;

      const keypair = localStorage.getItem("keypair");
      if (keypair === null) {
        // generates RSA keypair
        await forge.pki.rsa.generateKeyPair(
          { bits: 2048, workers: 2 },
          (err, keypair) => {
            this.keypair = {
              publicKey: Buffer.from(
                forge.pki.publicKeyToPem(keypair.publicKey)
              ).toString("base64"),
              privateKey: Buffer.from(
                forge.pki.privateKeyToPem(keypair.privateKey)
              ).toString("base64"),
            };
            localStorage.setItem("keypair", JSON.stringify(this.keypair));
            this.privateKey = keypair.privateKey;
          }
        );
      } else {
        this.keypair = JSON.parse(keypair);
        this.privateKey = Buffer.from(
          this.keypair.privateKey,
          "base64"
        ).toString();
        this.privateKey = forge.pki.privateKeyFromPem(this.privateKey);
      }

      // restore session
      await this.login();

      // join room
      socket.emit("join_room", {
        user: this.user,
      });

      // retrieve users from localStorage
      if (localStorage.getItem("users")) {
        this.users = JSON.parse(localStorage.getItem("users"));
      }
      this.loading = false;
    },
  },
  beforeMount() {
    this.load();
  },
  mounted() {
    // socket to receive messages
    socket.on("receive_message", (data) => {
      const message = decryptMessage(data.message, this.privateKey);

      let temp = [];
      if (localStorage.getItem(data.user)) {
        temp = JSON.parse(localStorage.getItem(data.user));
      }

      temp.push({ user: data.user, message: message });
      if (this.to === data.user) {
        this.messages = temp;
      } else if (!this.users.includes(data.user)) {
        // add to users if not present
        this.connect(data.user);
      }

      this.rearrange(data.user);
      this.setMessages(data.user, JSON.stringify(temp));
    });

    socket.on("room_announcements", (data) => {
      console.log(data);
    });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto&display=swap");
* {
  font-family: "Roboto", "Helvetica", sans-serif;
}

.inputBox:hover {
  cursor: pointer;
}

h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: list-item;
  margin: 0 10px;
}

a {
  color: #42b983;
}

button {
  border-radius: 0 15px 15px 0 !important;
  border: 0 !important;
}

input {
  border-radius: 15px 0 0 15px !important;
  border: 0 !important;
  background-color: rgba(255, 255, 255, 0.1);
  color: #f9f6f7;
}

input:focus {
  box-shadow: none !important;
  background-color: rgba(255, 255, 255, 0.05);
  color: #f9f6f7;
  outline: 0;
}

input::placeholder {
  color: gray;
}

.inputBox {
  margin-top: 0.4rem;
  border-radius: 10px;
  background-color: #23262a;
  padding: 0.1rem 0;
  opacity: 0.7;
}
.btn.focus,
.btn:focus {
  outline: 0;
  box-shadow: none !important;
}

.chat {
  border: 1px solid rgb(75, 70, 71) !important;
  padding: 0 !important;
  border-radius: 10px;
}

.card {
  border-radius: 10px !important;
  border: 1px double rgba(255, 255, 255, 0.1) !important;
  background-color: #0d1117;
  height: 85vh;
}

.card-header {
  border-radius: 10px 10px 0 0 !important;
  border: 0 !important;
  background-color: rgba(0, 0, 0, 0.2);
}

.card-footer {
  border-radius: 0 0 10px 10px !important;
  border: 0 !important;
  background-color: rgba(0, 0, 0, 0.4);
}

.msg_card_body {
  overflow-y: auto;
  height: 75vh;
}

.contact_body {
  border-radius: 15px !important;
  border: 1px double rgba(0, 0, 0, 0.3) !important;
  background-color: rgba(55, 55, 55, 0.1);
  text-align: center;
  padding: 1rem;
  width: 100%;
  color: #f9f6f7;
}

.text-a {
  color: #212529;
}

.text-b {
  color: #f9f6f7;
}

.color-a {
  background-color: #ffd700;
}

.color-b {
  background-color: #1f4287;
}

.msg_container {
  margin-top: auto;
  margin-bottom: auto;
  margin-left: 10px;
  border-radius: 25px;
  padding: 10px;
  position: relative;
  max-width: 75%;
  text-align: left;
}

.etrans {
  -webkit-transition: all 0.2s ease-out;
  -moz-transition: all 0.2s ease-out;
  -ms-transition: all 0.2s ease-out;
  -o-transition: all 0.2s ease-out;
  transition: all 0.2s ease-out;
}
</style>
