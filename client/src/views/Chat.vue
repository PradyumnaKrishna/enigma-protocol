<template>
  <clip-loader v-if="loading" :loading="loading" :color="color" :size="size"></clip-loader>
  <div v-else>
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

    <div v-else>
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
  </div>
</template>

<script>
import io from "socket.io-client";
import ClipLoader from "../assets/ClipLoader";

var fetch = require('node-fetch');
var socket = io.connect("http://localhost:5000");

export default {
  name: "Home",
  components: {
    ClipLoader
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

    load: async function () {
      this.loading = true;

      if (this.$cookies.isKey("user")) {
        if (await this.connect(this.$cookies.get("user"))) {
          this.user = this.$cookies.get("user");
        } else {
          await this.login();
        }
      } else {
        await this.login()
      }

      if (this.$cookies.isKey("to")) {
        if (await this.connect(this.$cookies.get("to"))) {
          this.to = this.$cookies.get("to");
        } else {
          this.$cookies.remove("to");
        }
      }

      this.loading = false;
    },

    send: function() {
      socket.emit('send_message', {
        user: this.$cookies.get("user"),
        message: this.message,
        to: this.to
      });
      this.messages.push({ user: "self", message: this.message });
      this.message = "";
    },

    join_room: async function() {
        if ((this.room != this.$cookies.get("user")) && (await this.connect(this.room))) { 
          this.to = this.room;
          this.$cookies.set("to", this.to);
          console.log("user is connected");
        } else {
            alert("Wrong user")
        }
    }
  },
  mounted() {
    var self = this;
    self.load();

    socket.on("connect", function () {
      socket.emit("join_room", {
        user: self.$cookies.get("user"),
      });
      console.log("socket connect")
    })

    socket.on('receive_message', function(data) {
      self.messages.push({ user: data.user, message: data.message });
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
