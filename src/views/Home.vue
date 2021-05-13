<template>
  <ul id="messages"></ul>
  <input type="text" id="myMessage" />
  <button id="sendbutton">Send</button>
</template>

<script>
import io from "socket.io-client";
import $ from 'jquery';
var fetch = require('node-fetch');
var socket = io.connect("http://localhost:5000");

export default {
  name: "Home",
  props: {
    msg: String,
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
      fetch(`http://localhost:500/login/$(this.user)`)
        .then(response => response.json())
        .then(json => {
          if (json.status) {
            return
          } else {
            this.login();
            this.$cookies.set("user", this.user);
          }
        });
    }
  },
  mounted() {
    if (this.$cookies.isKey("user")) {
      this.check()
    } else {
      this.login()
    }

    socket.on("connect", function () {
      socket.send("User has connected!");
    });

    socket.on("message", function (msg) {
      $("#messages").append("<li>" + msg + "</li>");
      console.log("Received message");
    });

    $("#sendbutton").on("click", function () {
      socket.send($("#myMessage").val());
      $("#myMessage").val("");
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
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
