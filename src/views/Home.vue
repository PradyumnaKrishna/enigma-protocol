<template>
  <ul id="messages">
    <li v-for="message in messages" :key="message">
      {{ message }}
    </li>
  </ul>
  <form v-on:submit.prevent="onSubmit" class="form">
    <input v-model="message" placeholder="Message"/>
    <button @click="send">Send</button>
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
    login: function() {
      fetch('http://localhost:5000/login')
        .then(response => response.json())
        .then(json => {
          this.user = json.user;
          this.$cookies.set("user", this.user);
        });
    },

    check: function() {
      this.user = this.$cookies.get("user");
      fetch('http://localhost:5000/login/'+this.user)
        .then(response => response.json())
        .then(json => {
          if (json.status) {
            return
          } else {
            this.login();
            this.$cookies.set("user", this.user);
          }
        });
    },

    send: function() {
      socket.send(this.message);
      this.message = "";
    },

    add: function(msg) {
      this.items.push(msg)
    }
  },
  mounted() {
    var self=this

    if (self.$cookies.isKey("user")) {
      self.check()
    } else {
      self.login()
    }

    socket.on("connect", function () {
      socket.send("User has connected!");
    });

    socket.on("message", function (msg) {
      self.messages.push(msg);
      console.log("Received message");
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
