<template>
  <clip-loader v-if="loading"></clip-loader>
  <div v-else>
    <div class="d-flex justify-content-center">
      <div class="row justify-content-center h-75 w-100">
        <div class="col-md-4 col-xl-3 chat">
          <div class="card mb-sm-3 mb-md-0 h-100 contacts_card">
            <div class="card-header">
              <p>
                <strong>{{ user }}</strong>
              </p>
              <form v-on:submit.prevent="onSubmit" class="form">
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control search"
                    v-model="room"
                    placeholder="Other User's ID"
                  />
                  <div class="input-group-prepend">
                    <button
                      class="btn btn-dark"
                      style="color: #78e08f"
                      @click="join_room"
                    >
                      <strong>Add</strong>
                    </button>
                  </div>
                </div>
              </form>
            </div>
            <div class="card-body contacts_body">
              <div class="contacts">
                <button
                  class="contact_body"
                  v-for="contact in users"
                  :key="contact"
                  :style="
                    contact === to
                      ? { 'background-color': 'rgba(255,255,255,0.1)' }
                      : null
                  "
                  @click="switchTo(contact)"
                >
                  {{ contact }}
                </button>
              </div>
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
              <form v-if="to" v-on:submit.prevent="onSubmit" class="form">
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control"
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
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import io from "socket.io-client";
import ClipLoader from "../assets/ClipLoader";

URL = "https://enigma-protocol.azurewebsites.net";

const forge = require("node-forge");
const fetch = require("node-fetch");
const socket = io.connect(URL);

export default {
  name: "Home",
  components: {
    ClipLoader,
  },
  props: {
    room: String,
  },
  data() {
    return {
      loading: true,
      messages: [],
      message: "",
      users: [],
      user: null,
      to: null,
    };
  },
  methods: {
    copy: async function (text) {
      await navigator.clipboard.writeText(text);
      alert("Text Copied");
    },
    
    login: async function () {
      const response = await fetch(
        `${URL}/login/${this.$cookies.get("publicKey")}`
      );
      const json = await response.json();
      this.user = json.user;
      this.$cookies.set("user", this.user);
    },

    connect: async function (user) {
      const response = await fetch(`${URL}/connect/${user}`);
      return await response.json();
    },

    retreive: function (type, value) {
      if (localStorage.getItem(value)) {
        try {
          this[type] = JSON.parse(localStorage.getItem(value))
        } catch (e) {
          localStorage.removeItem(value);
        }
      }
    },

    join_room: async function () {
      const json = await this.connect(this.room);
      if (this.room !== this.user && json.status) {
        this.to = this.room;
        this.$cookies.set("to", this.to);
        this.$cookies.set(json.to, json.publicKey);
        this[this.to] = Buffer.from(json.publicKey, "base64").toString();
        console.log("user is connected");

        if (!this.users.includes(this.to)) {
          this.users.push(this.to);
          const parsed = JSON.stringify(this.users);
          localStorage.setItem("users", parsed);
        }
      } else {
        alert("Wrong user");
      }
    },

    switchTo: async function (id) {
      this.to = id;
      await this.retreive("messages", id);
      const publicKey = this.$cookies.get(this.to);
      this[this.to] = Buffer.from(publicKey, "base64").toString();
      this.publicKey = forge.pki.publicKeyFromPem(this[this.to]);

      const container = this.$refs.messages;
      container.scrollTop = container.scrollHeight;
    },

    send: async function () {
      const message = this.publicKey.encrypt(this.message);
      socket.emit("send_message", {
        user: this.$cookies.get("user"),
        message: message,
        to: this.to,
      });
      await this.messages.push({ user: "self", message: this.message });
      this.setMessages(this.to, JSON.stringify(this.messages))
      this.message = "";
    },

    setMessages: function (user, parsed) {
      localStorage.setItem(user, parsed);

      const container = this.$refs.messages;
      container.scrollTop = container.scrollHeight;
    },

    load: async function () {
      this.loading = true;

      if (this.$cookies.isKey("privateKey")) {
        this.privateKey = Buffer.from(this.$cookies.get("privateKey"), "base64").toString();
        this.privateKey = forge.pki.privateKeyFromPem(this.privateKey);
      } else {
        await forge.pki.rsa.generateKeyPair({ bits: 2048, workers: 2 }, (err, keypair) => {
            this.publicKey = forge.pki.publicKeyToPem(keypair.publicKey);
            this.$cookies.set("publicKey", Buffer.from(this.publicKey).toString("base64"));

            this.privateKey = keypair.privateKey;
            const key = forge.pki.privateKeyToPem(keypair.privateKey);
            this.$cookies.set("privateKey", Buffer.from(key).toString("base64"));
        });
      }

      if (this.$cookies.isKey("user")) {
        const json = await this.connect(this.$cookies.get("user"));
        if (json.status) {
          this.user = this.$cookies.get("user");
        } else {
          await this.login();
        }
      } else {
        await this.login();
      }

      const user = this.$cookies.get("user");
      socket.emit("join_room", {
        user: user,
      });

      this.retreive("users", "users");
      this.loading = false;
    },
  },
  beforeMount() {
    this.load();
  },
  mounted() {
    socket.on("receive_message", (data) => {
      const message = this.privateKey.decrypt(data.message);

      let temp = [];
      if (localStorage.getItem(data.user)) {
        temp = JSON.parse(localStorage.getItem(data.user));
      }

      temp.push({ user: data.user, message: message });
      if (this.to === data.user) {
        this.messages = temp;
      }

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
  -webkit-transition: all 0.2s ease-out;
  -moz-transition: all 0.2s ease-out;
  -ms-transition: all 0.2s ease-out;
  -o-transition: all 0.2s ease-out;
  transition: all 0.2s ease-out;
}

input:focus {
  box-shadow: none !important;
  background-color: rgba(255, 255, 255, 0.05);
  color: #f9f6f7;
  outline: 0;
}

.btn.focus,
.btn:focus {
  outline: 0;
  box-shadow: none !important;
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
</style>
