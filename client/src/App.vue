<template>
  <div id="nav">
    <router-link to="/">Home</router-link> |
    <router-link to="/chat">Chat</router-link> |
    <router-link to="/docs">Docs</router-link>
  </div>

  <section class="section">
    <router-view/>
  </section>
</template>

<style lang="scss">
body, html {
  background: #080808;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  background: #080808;
  color: #F9F6F7;
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
    color: #ECECEC;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
