<script>
import Home from './components/Home.vue'
import Chat from './components/Chat.vue'
import ClipLoader from './components/ui/ClipLoader.vue'
import Crypto from './utils/crypto'
import Storage from './utils/storage'

const URL = import.meta.env.VITE_API_URL

export default {
  name: 'App',
  components: {
    Home,
    Chat,
    ClipLoader,
  },
  data() {
    return {
      loading: true,
      keypair: null,
      user: null,
      hosts: [],
      host: null,
    }
  },
  mounted() {
    this.hosts = [URL]
    if (URL.startsWith('https://')) {
      this.host = {
        url: URL.replace('https://', ''),
        secure: true,
      }
    } else if (URL.startsWith('http://')) {
      this.host = {
        url: URL.replace('http://', ''),
        secure: false,
      }
    } else {
      this.host = {
        url: URL,
        secure: false,
      }
    }

    this.keypair = Storage.getKeypair()
    if (this.keypair) {
      this.user = this.$cookies.get('user')
    }
    this.loading = false
  },
  methods: {
    async initiateProtocol() {
      this.loading = true
      this.keypair = Crypto.generateKeypair()
      Storage.setKeypair(this.keypair)

      const publicKey = this.keypair.publicKey
      fetch(`${URL}/login/${publicKey}`)
        .then((response) => response.json())
        .then((data) => {
          this.$cookies.set('user', data.user)
          this.user = data.user
          this.loading = false
        })
        .catch((error) => {
          console.error('Error:', error)
          this.loading = false
        })
    },
    invalidUser() {
      this.$cookies.remove('user')
      this.user = null
    },
  },
}
</script>

<template>
  <main>
    <clip-loader v-if="loading" />
    <div v-else>
      <Home v-if="!user" @initiate="initiateProtocol" />
      <Chat v-else :keypair="keypair" :user="user" :host="host" @invalidUser="invalidUser" />
    </div>
  </main>
</template>

<style>
body,
html {
  background: #080808;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background: #080808;
  color: #f9f6f7;
}

.container {
  padding: auto;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

p {
  font-size: 20px;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #ececec;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
