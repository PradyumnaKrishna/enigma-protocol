<template>
  <clip-loader v-if="loading"></clip-loader>
  <div v-else>
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
            <button class="btn btn-primary" @click="join_room">Send</button>
          </div>
        </div>
      </form>
    </div>

    <div v-else>
      <ul id="messages">
        <li v-for="item in messages" :key="item.message">
          {{ item.user }}: {{ item.message }}
        </li>
      </ul>
      <form v-on:submit.prevent="onSubmit" class="form">
        <div class="container input-group w-50 mb-3">
          <input
            type="text"
            class="form-control"
            v-model="message"
            placeholder="Message"
          />
          <div class="input-group-append">
            <button class="btn btn-primary" @click="send">Send</button>
          </div>
        </div>
      </form>
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
      this.messages.push({ user: "self", message: this.message });
      this.message = "";
    },

    join_room: async function () {
      var json = await this.connect(this.room);
      if (
        this.room != this.$cookies.get("user") &&
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
  },
  mounted() {
    var self = this;
    self.load();

    socket.on("connect", function () {
      socket.emit("join_room", {
        user: self.$cookies.get("user"),
      });
      console.log("socket connect");
    });

    socket.on("receive_message", function (data) {
      var key = forge.pki.privateKeyFromPem(self.privateKey);
      var message = key.decrypt(data.message);
      self.messages.push({ user: data.user, message: message });
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
</style>
