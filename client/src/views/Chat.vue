<template>
  <clip-loader v-if="loading"></clip-loader>
  <div v-else>
    <div class="container w-75 d-flex px-5">
      <div class="row justify-content-between w-100">
        <div class="col text-start">
          <button class="shadow btn color-b" @click="copy(user)"><strong>User: {{ user }}</strong></button>
        </div>
        <div class="col text-end">
          <button class="shadow btn color-a" @click="copy(to)"><strong>Connected To: {{ to }}</strong></button>
        </div>
      </div>
    </div>
    <div v-if="!to">
      <form v-on:submit.prevent="onSubmit" class="form">
        <div class="container input-group w-50 mb-3">
          <input
              type="text"
              class="form-control"
              v-model="room"
              placeholder="Other User ID"
          />
          <div class="input-group-append">
            <button class="btn btn-dark" style="color: #78e08f;" @click="join_room"><strong>Send</strong></button>
          </div>
        </div>
      </form>
    </div>

    <div v-else class="d-flex justify-content-center">
      <div class="card w-50">
        <div ref="messages" class="card-body msg_card_body">
          <div v-for="item in messages" :key="item.message">
            <div v-if="item.user === 'self'" class="d-flex justify-content-end mb-4">
              <div class="msg_container color-b">
                {{ item.message }}
              </div>
            </div>
            <div v-else class="d-flex justify-content-start mb-4">
              <div class="msg_container color-a">
                {{ item.message }}
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <form v-on:submit.prevent="onSubmit" class="form">
            <div class="input-group">
              <input
                  type="text"
                  class="form-control"
                  v-model="message"
                  placeholder="Message"
              />
              <div class="input-group-append">
                <button v-bind:disabled="!message" class="btn btn-dark" style="color: #78e08f;" @click="send"><strong>Send</strong>
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import io from "socket.io-client";
import ClipLoader from "../assets/ClipLoader";

let URL = process.env.URL;
if (!URL) {
  URL = "https://enigma-protocol.azurewebsites.net"
}

const forge = require("node-forge")
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
      user: null,
      to: null,
    };
  },
  methods: {
    login: async function () {
      const response = await fetch(`${URL}/login/${this.$cookies.get("publicKey")}`);
      const json = await response.json();
      this.user = json.user;
      this.$cookies.set("user", this.user);
    },

    connect: async function (user) {
      const response = await fetch(`${URL}/connect/${user}`);
      return await response.json();
    },
    
    retreive: function () {
      if (localStorage.getItem(this.to)) {
        try {
          this.messages = JSON.parse(localStorage.getItem(this.to));
        } catch(e) {
          localStorage.removeItem(this.to);
        }
      }
    },

    load: async function () {
      this.loading = true;

      if (this.$cookies.isKey("privateKey")) {
        this.privateKey = Buffer.from(this.$cookies.get("privateKey"), 'base64').toString();
        this.privateKey = forge.pki.privateKeyFromPem(this.privateKey);
      } else {
        await forge.pki.rsa.generateKeyPair({bits: 2048, workers: 2}, (err, keypair) => {
          this.publicKey = forge.pki.publicKeyToPem(keypair.publicKey);
          this.$cookies.set("publicKey", Buffer.from(this.publicKey).toString("base64"));

          this.privateKey = keypair.privateKey
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

      if (this.$cookies.isKey("to")) {
        const json = await this.connect(this.$cookies.get("to"));
        if (json.status) {
          this.to = this.$cookies.get("to");
          this[this.to] = Buffer.from(json.publicKey, 'base64').toString();
          this.retreive();
        } else {
          this.$cookies.remove("to");
        }
      }

      this.loading = false;
    },

    send: function () {
      const key = forge.pki.publicKeyFromPem(this[this.to]);
      const message = key.encrypt(this.message);
      socket.emit("send_message", {
        user: this.$cookies.get("user"),
        message: message,
        to: this.to,
      });
      this.addMessage({user: "self", message: this.message});
      this.message = "";
    },

    join_room: async function () {
      const json = await this.connect(this.room);
      if (
          this.room !== this.user &&
          json.status
      ) {
        this.to = this.room;
        this.$cookies.set("to", this.to);
        this.$cookies.set(json.to, json.publicKey);
        this[this.to] = Buffer.from(json.publicKey, 'base64').toString();
        console.log("user is connected");
      } else {
        alert("Wrong user");
      }
    },

    copy: async function (user) {
      await navigator.clipboard.writeText(user);
      alert("Text Copied");
    },

    addMessage: function (json) {
      this.messages.push(json) //adding new message to the list
      this.$nextTick(function () {
        const container = this.$refs.messages;
        container.scrollTop = container.scrollHeight;
      })

      const parsed = JSON.stringify(this.messages);
      localStorage.setItem(this.to, parsed);
    },
  },
  beforeMount() {
    this.load();
  },
  mounted() {
    socket.on("receive_message", (data) => {
      const message = this.privateKey.decrypt(data.message);
      this.addMessage({user: data.user, message: message});
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

.msg_card_body {
  overflow-y: auto;
  height: 75vh;
}

.color-a {
  background-color: #82ccdd;
}

.color-b {
  background-color: #78e08f;
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
