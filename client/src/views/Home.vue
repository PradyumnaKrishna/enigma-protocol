<template>
  <ul id="messages">
    <li v-for="message in messages" :key="message">
      {{ message }}
    </li>
  </ul>
  <form v-on:submit.prevent="onSubmit" class="form">
    <div class="container input-group w-50 mb-3">
      <input type="text" class="form-control" v-model="message" placeholder="Message">
      <div class="input-group-append">
        <button class="btn btn-primary" @click="send">Send</button>
      </div>
    </div>
  </form>
</template>

<script>
import io from "socket.io-client";
var fetch = require('node-fetch');
var socket = io.connect("http://localhost:5000");

export default {
  name: "Home",
  props: {
    msg: String,
  },
  data() {
    return {
      messages: [],
      message: ""
    };
  },
  methods: {
    login: async function() {
      const response = await fetch('http://localhost:5000/login');
      const json = await response.json();
      this.user = json.user;
      this.$cookies.set("user", this.user);
    },

    connect: async function(user) {
      const response = await fetch(`http://localhost:5000/connect/${user}`);
      const json = await response.json();
      if (json.status) {
        this.user = this.$cookies.get("user");
      } else {
        await this.login();
      }
    },

    send: function() {
      socket.send(this.message);
      this.message = "";
    },
  },
  async mounted() {
    if (this.$cookies.isKey("user")) {
      await this.connect(this.$cookies.get("user"))
    } else {
      await this.login()
    }

    var self = this;

    socket.on("connect", function () {
      socket.send(`${self.user} has connected!`);
    });

    socket.on("message", function (msg) {
      self.messages.push(msg);
      console.log("Received message");
    });

    socket.on("disconnect", function () {
      socket.send(`${self.user} has disconnected!`);
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
