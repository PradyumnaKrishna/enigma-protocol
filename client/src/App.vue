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
  border-top: 1px solid #ECECEC;
  border-bottom: 1px solid #ECECEC;
}

#nav a {
  font-weight: bold;
  color: #ECECEC;
  margin: 0 10px;
  padding: 5px;
  border: 1px solid transparent;
  border-radius: 4px;
  transition: color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
}

#nav a.router-link-exact-active {
  color: #42b983;
  background-color: #ECECEC;
  border-color: #42b983;
}

#nav a:hover {
  color: #42b983;
  background-color: #ECECEC;
  border-color: #42b983;
}

</style>
