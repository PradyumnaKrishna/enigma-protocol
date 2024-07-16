<template>
  <div class="container mx-auto w-1/2">
    <h1 class="text-4xl font-medium">Enigma Protocol</h1>
    <br />
    <p>
      This Website is used for anonymous chatting with end-to-end encryption support. I can't
      decrypt those messages because they are encrypted using the client side of the web
      application.
    </p>
    <br />
    <button
      class="text-[#42b983] bg-gray-800 hover:bg-black border border-gray-800 focus:outline-none focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2"
      @click="initiateProtocol"
    >
      Initiate Protocol
    </button>
  </div>
</template>

<script>
export default {
  name: 'HomeComponent',
  methods: {
    initiateProtocol() {
      this.$emit('initiate')
    },
  },
}
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
