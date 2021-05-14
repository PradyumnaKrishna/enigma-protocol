<template>
  <div v-if="!to">
    <form v-on:submit.prevent="onSubmit" class="form">
      <div class="container input-group w-50 mb-3">
        <input type="text" class="form-control" v-model="room" placeholder="Other User ID">
        <div class="input-group-append">
          <button class="btn btn-primary" @click="join_room">Send</button>
        </div>
      </div>
    </form>
  </div>

  <div v-if="to">
    <ul id="messages">
      <li v-for="item in messages" :key="item.message">
        {{item.user}}: {{ item.message }}
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
  </div>
</template>

<script>
import io from "socket.io-client";
var fetch = require('node-fetch');
var socket = io.connect("http://localhost:5000");

export default {
  name: "Home",
  props: {
    room: String,
  },
  data() {
    return {
      messages: [],
      message: "",
      to: null,
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
      return json.status
    },

    send: function() {
      socket.emit('send_message', {
        user: this.$cookies.get("user"),
        message: this.message,
        to: this.to
      });
      this.message = "";
    },

    join_room: async function() {
        if ((this.room != this.$cookies.get("user")) && (await this.connect(this.room))) { 
          this.to = this.room;
          socket.emit("join_room", {
            user: this.$cookies.get("user"),
            room: this.to
          });
          console.log("user is connected");
        } else {
            alert("Wrong user")
        }
    }
  },
  async mounted() {
    if (this.$cookies.isKey("user")) {
      if (!this.connect(this.$cookies.get("user"))) {
          await this.login();
      }
    } else {
      await this.login()
    }

    var self = this;

    socket.on("connect", function () {
      console.log("socket connect")
    })

    socket.on('receive_message', function(data) {
      self.messages.push({ user: data.user, message: data.message })
    });

    socket.on('room_announcements', function(data) {
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
