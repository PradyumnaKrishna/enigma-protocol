<template>
  <ToastMessage :toastmsg="toastmsg" :toastType="toastType" />
  <div class="flex justify-center h-screen items-center">
    <div class="flex flex-wrap justify-center w-full">
      <div class="md:w-1/3 pr-4 pl-4 xl:w-1/4 chat">
        <div class="h-[85vh] flex flex-col">
          <UserInfo :user="user" @requestCopy="copy" @joinRoom="join_room" />
          <ChatListHeader :users="users" :activeUser="to" @switch="switchTo" />
        </div>
      </div>
      <div class="md:w-2/3 pr-4 pl-4 xl:w-1/2 chat h-full">
        <div class="card">
          <div class="card-header">
            <div class="flex">
              <p class="text-b ml-3 mt-3">
                <strong>{{ to }}</strong>
              </p>
            </div>
          </div>
          <div ref="messages" class="card-body msg_card_body">
            <div v-if="!to">
              <img class="mx-auto" src="../assets/logo.png" />
              <p style="color: #42b983">
                <strong>Protocol Initiated</strong>
              </p>
            </div>
            <div v-else v-for="item in messages" :key="item">
              <div v-if="item.user === 'self'" class="flex justify-end mb-4">
                <div class="msg_container color-b text-b">
                  {{ item.message }}
                </div>
              </div>
              <div v-else class="flex justify-start mb-4">
                <div class="msg_container color-a text-a">
                  {{ item.message }}
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer">
            <MessageForm v-if="to && !isMessageFormDisabled" @sendMessage="send" />
            <p v-if="isMessageFormDisabled" style="color: #6c757d; font-weight: bold">
              {{ inactiveUserMessage }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ToastMessage from './ui/ToastMessage.vue'
import UserInfo from './chat/UserInfo.vue'
import MessageForm from './chat/MessageForm.vue'
// import ClipLoader from '../assets/ClipLoader'
import ChatListHeader from './chat/ChatListHeader.vue'

import Crypto from '../utils/crypto'

export default {
  name: 'ChatComponent',
  components: {
    UserInfo,
    ChatListHeader,
    ToastMessage,
    MessageForm,
  },
  props: {
    keypair: {
      publicKey: String,
      privateKey: String,
    },
    user: String,
    host: {
      secure: Boolean,
      url: String,
    },
  },
  data() {
    return {
      isMessageFormDisabled: false,
      inactiveUserMessage: '',
      loading: true,
      messages: [],
      users: [],
      toastmsg: '',
      toastType: '',
      to: null,
      room: null,
      privateKey: null,
      socket: null,
      wsURL: null,
      apiURL: null,
    }
  },
  methods: {
    copy: async function (text) {
      // finction to copy text to clipboard
      await navigator.clipboard.writeText(text)
      this.toastmsg = 'Text Copied'
      this.toastType = 'success'

      setTimeout(() => {
        this.toastmsg = ''
        this.toastType = ''
      }, 2000)
    },

    validateUser() {
      fetch(`${this.apiURL}/connect/${this.$props.user}`)
        .then((response) => response.json())
        .then((json) => {
          if (this.$props.keypair.publicKey !== json.publicKey) {
            this.$emit('invalidUser')
          }
        })
        .catch((err) => {
          console.error(err)
        })
    },

    connect: async function (user) {
      // function to set publicKey of user and return status
      let publicKey = fetch(`${this.apiURL}/connect/${user}`)
        .then((response) => response.json())
        .then((json) => {
          return json.publicKey
        })
        .catch((err) => {
          console.error(err)
        })

      return publicKey
    },

    retrieve: function (user) {
      // function retrieve messages from localStorage
      if (localStorage.getItem(user)) {
        try {
          this.messages = JSON.parse(localStorage.getItem(user))
        } catch (e) {
          localStorage.removeItem(user)
        }
      } else {
        this.messages = []
      }
    },

    join_room: async function (user) {
      // make connection with other user
      const response = await this.connect(user)
      console.log(response)
      if (user !== this.user && response) {
        this.rearrange(user)
        this.switchTo(user)
      } else {
        this.toastmsg = 'Wrong user'
        this.toastType = 'error'

        setTimeout(() => {
          this.toastmsg = ''
          this.toastType = ''
        }, 2000)
      }
    },

    switchTo: async function (user) {
      // switch to the user select
      this.to = user
      await this.retrieve(user)

      let publicKey = this.$cookies.get(user)
      if (!publicKey || typeof publicKey !== 'string') {
        publicKey = await this.connect(user)
        if (publicKey) {
          this.$cookies.set(user, publicKey)
        } else {
          this.isMessageFormDisabled = true
          this.inactiveUserMessage = 'User is inactive'
          return
        }
      }

      this.isMessageFormDisabled = false
      this.inactiveUserMessage = ''
      this.publicKey = Crypto.publicKeyFromBase64(publicKey)

      const container = this.$refs.messages
      container.scrollTop = container.scrollHeight
    },

    send: async function (text) {
      const message = Crypto.encryptMessage(text, this.publicKey)

      const data = JSON.stringify({
        from: this.user,
        payload: message,
        to: this.to,
      })

      this.socket.send(data)

      await this.messages.push({ user: 'self', message: text })
      this.setMessages(this.to, JSON.stringify(this.messages))
      this.rearrange(this.to)
    },

    setMessages: function (user, parsed) {
      // autoscroll to the bottom of container
      localStorage.setItem(user, parsed)

      const container = this.$refs.messages
      container.scrollTop = container.scrollHeight
    },

    rearrange: function (user) {
      // rearrange user
      const users = this.users.slice()
      users.unshift(user)

      this.users = [...new Set(users)]
      const parsed = JSON.stringify(this.users)
      localStorage.setItem('users', parsed)
    },
  },
  async mounted() {
    if (this.$props.host.secure) {
      this.wsURL = `wss://${this.$props.host.url}`
      this.apiURL = `https://${this.$props.host.url}`
    } else {
      this.wsURL = `ws://${this.$props.host.url}`
      this.apiURL = `http://${this.$props.host.url}`
    }

    this.validateUser()
    this.privateKey = Crypto.privateKeyFromBase64(this.$props.keypair.privateKey)

    const socket = new WebSocket(`${this.wsURL}/connect/${this.$props.user}`)

    // retrieve users from localStorage
    if (localStorage.getItem('users')) {
      this.users = JSON.parse(localStorage.getItem('users'))
    }
    this.loading = false

    // socket to send messages
    socket.onopen = () => {
      console.log('Connected to server')
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if ('error' in data) {
        console.log(data)
        return
      }

      const message = Crypto.decryptMessage(data.payload, this.privateKey)

      let temp = []
      if (localStorage.getItem(data.from)) {
        temp = JSON.parse(localStorage.getItem(data.from))
      }

      temp.push({ user: data.from, message: message })
      if (this.to === data.from) {
        this.messages = temp
      } else if (!this.users.includes(data.from)) {
        // add to users if not present
        this.connect(data.from)
      }

      this.rearrange(data.from)
      this.setMessages(data.from, JSON.stringify(temp))
    }

    socket.onclose = () => {
      console.log('Disconnected from server')
      this.toastmsg = 'Disconnected from server'
      this.toastType = 'error'

      setTimeout(() => {
        this.toastmsg = ''
        this.toastType = ''
      }, 2000)
    }

    this.socket = socket
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
* {
  font-family: 'Roboto', 'Helvetica', sans-serif;
}

.inputBox:hover {
  cursor: pointer;
}

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
}

input:focus {
  box-shadow: none !important;
  background-color: rgba(255, 255, 255, 0.05);
  color: #f9f6f7;
  outline: 0;
}

input::placeholder {
  color: gray;
}

.inputBox {
  margin-top: 0.4rem;
  border-radius: 10px;
  background-color: #23262a;
  padding: 0.1rem 0;
  opacity: 0.7;
}
.btn.focus,
.btn:focus {
  outline: 0;
  box-shadow: none !important;
}

.chat {
  border: 1px solid rgb(75, 70, 71) !important;
  padding: 0 !important;
  border-radius: 10px;
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

.etrans {
  -webkit-transition: all 0.2s ease-out;
  -moz-transition: all 0.2s ease-out;
  -ms-transition: all 0.2s ease-out;
  -o-transition: all 0.2s ease-out;
  transition: all 0.2s ease-out;
}
</style>
