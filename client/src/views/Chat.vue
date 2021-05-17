<template>
  <clip-loader v-if="loading"></clip-loader>
  <div v-else>
    <div class="container w-75 d-flex px-5">
      <div class="row justify-content-between w-100">
        <div class="col text-start">
          <button class="shadow btn color-b" @click="copy(user)"><p class="my-0"><strong>User: {{ user }}</strong></p></button>
        </div>
        <div class="col text-end">
          <button class="shadow btn color-a" @click="copy(to)"><p class="my-0"><strong>Connected To: {{ to }}</strong></p></button>
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
              <div class="msg_cotainer color-b">
                {{ item.message }}
              </div>
            </div>
            <div v-else class="d-flex justify-content-start mb-4">
              <div class="msg_cotainer color-a">
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
                <button v-bind:disabled="!message" class="btn btn-dark" style="color: #78e08f;" @click="send"><strong>Send</strong></button>
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

var forge = require("node-forge")
var fetch = require("node-fetch");
var socket = io.connect("http://localhost:5000");

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
      const response = await fetch(`http://localhost:5000/login/${this.$cookies.get("publicKey")}`);
      const json = await response.json();
      this.user = json.user;
      this.$cookies.set("user", this.user);
    },

    connect: async function (user) {
      const response = await fetch(`http://localhost:5000/connect/${user}`);
      const json = await response.json();
      return json;
    },

    load: async function () {
      this.loading = true;

      if (this.$cookies.isKey("privateKey")) {
        this.privateKey = Buffer.from(this.$cookies.get("privateKey"), 'base64').toString();
      } else {
        var self = this;
        await forge.pki.rsa.generateKeyPair({bits: 2048, workers: 2}, function(err, keypair) {
          self.publicKey = forge.pki.publicKeyToPem(keypair.publicKey); 
          self.$cookies.set("publicKey", Buffer.from(self.publicKey).toString("base64"));

          self.privateKey = forge.pki.privateKeyToPem(keypair.privateKey); 
          self.$cookies.set("privateKey", Buffer.from(self.privateKey).toString("base64"));
        });
      }

      if (this.$cookies.isKey("user")) {
        var json = await this.connect(this.$cookies.get("user"));
        if (json.status) {
          this.user = this.$cookies.get("user");
        } else {
          await this.login();
        }
      } else {
        await this.login();
      }

      var user = this.$cookies.get("user");
      socket.emit("join_room", {
        user: user,
      });

      if (this.$cookies.isKey("to")) {
        var json = await this.connect(this.$cookies.get("to"));
        if (json.status) {
          this.to = this.$cookies.get("to");
          this[this.to] = Buffer.from(json.publicKey, 'base64').toString();
        } else {
          this.$cookies.remove("to");
        }
      }

      this.loading = false;
    },

    send: function () {
      var key = forge.pki.publicKeyFromPem(this[this.to]);
      var message = key.encrypt(this.message);
      socket.emit("send_message", {
        user: this.$cookies.get("user"),
        message: message,
        to: this.to,
      });
      this.addMessage({ user: "self", message: this.message });
      this.message = "";
    },

    join_room: async function () {
      var json = await this.connect(this.room);
      if (
        this.room != this.user &&
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
          var container = this.$refs.messages;
          container.scrollTop = container.scrollHeight;
      })
    },
  },
  beforeMount() {
    this.load();
  },
  mounted() {
    var self = this;

    socket.on("receive_message", function (data) {
      var key = forge.pki.privateKeyFromPem(self.privateKey);
      var message = key.decrypt(data.message);
      self.addMessage({ user: data.user, message: message });
    });

    socket.on("room_announcements", function (data) {
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

.msg_card_body{
  overflow-y: auto;
  height: 75vh;
}

.color-a {
  background-color: #82ccdd;
}

.color-b {
  background-color: #78e08f;
}

.msg_cotainer{
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
