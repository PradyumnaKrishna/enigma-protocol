<template>
  <ul id="messages"></ul>
  <input type="text" id="myMessage" />
  <button id="sendbutton">Send</button>
</template>

<script>
import io from "socket.io-client";
import $ from 'jquery';
var socket = io.connect("http://localhost:5000");

export default {
  name: "Home",
  props: {
    msg: String,
  },
  mounted() {

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
