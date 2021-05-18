<template>
  <div class="container about w-50 mx-auto">
    <h1>Enigma Protocol</h1>
    <br/>
    <p>
      This Website is used for anonymous chatting with end to end encryption support.
      I can't decrypt those message because they are encrypted using client side of
      the web application.
    </p>
    <br/>
    <router-link to="chat" class="btn btn-dark">Initiate Protocol</router-link>
  </div>
</template>

<script>

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
  mounted() {
  }
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
