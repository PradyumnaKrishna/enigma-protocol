<template>
  <ToastMessage :toastmsg="toastmsg" :toastType="toastType" />
  <div class="flex justify-center h-screen items-center">
    <div class="inline-flex justify-center w-full gap-2">
      <div class="md:w-1/3 xl:w-1/4 chat border border-gray-700 rounded-lg">
        <div class="h-[85vh] flex flex-col">
          <UserInfo :user="user" @requestCopy="copy" @joinRoom="join_room" />
          <ChatListHeader :users="users" :activeUser="to" @switch="switchTo" />
        </div>
      </div>
      <div class="md:w-2/3 xl:w-1/2 chat h-full border border-gray-700 rounded-lg">
        <div class="h-[85vh] flex flex-col">
          <div>
            <p class="text-b ml-3 mt-3">
              <strong>{{ to }}</strong>
            </p>
          </div>
          <div ref="messages" class="h-full text-left overflow-hidden overflow-y-auto">
            <div v-if="!to" class="text-center">
              <img class="mx-auto" src="../assets/logo.png" />
              <p style="color: #42b983">
                <strong>Protocol Initiated</strong>
              </p>
            </div>
            <div v-else v-for="item in messages" :key="item">
              <div
                class="flex mb-4 mx-2"
                :class="[item.user === 'self' ? 'justify-end' : 'justify-start']"
              >
                <div
                  class="py-2 px-3 rounded-2xl"
                  :class="[
                    item.user === 'self'
                      ? 'bg-[#1f4287] text-[#f9f6f7] ml-10'
                      : 'bg-[#ffd700] text-[#212529] mr-10',
                  ]"
                >
                  {{ item.message }}
                </div>
              </div>
            </div>
          </div>
          <div>
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

    const socket = new WebSocket(`${this.wsURL}/ws/${this.$props.user}`)

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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
* {
  font-family: 'Roboto', 'Helvetica', sans-serif;
}
</style>
