<template>
  <div>
    <p id="userId" class="inputBox">
      User ID :
      <strong
        class="clickableUserId"
        @click="copy(user)"
        title="click to copy"
        >{{ user }}</strong
      >
    </p>
    <form v-on:submit.prevent="onSubmit" class="form">
      <div class="input-group">
        <input
          type="text"
          class="form-control etrans"
          required
          v-model="room"
          placeholder="Other User's ID"
        />
        <div class="input-group-prepend">
          <button class="btn btn-dark" @click="joinRoom">
            <strong>Add</strong>
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "UserInfo",
  props: {
    user: String,
  },
  data() {
    return {
      room: "",
    };
  },
  methods: {
    copy(userId) {
      // Emit the event to parent component to handle the copy action
      this.$emit("requestCopy", userId);
    },
    joinRoom() {
      // Emit the joinRoom event with the room ID
      this.$emit("joinRoom", this.room);
    },
    onSubmit() {
      // If the form is submitted, trigger the join room logic
      this.joinRoom();
    },
  },
};
</script>

<style scoped>

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

button {
  border-radius: 0 15px 15px 0 !important;
  border: 0 !important;
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

.clickableUserId {
  text-decoration: underline;
  cursor: pointer;
  transition: color 0.3s ease;
}

.clickableUserId:hover {
  color: #42b983;
}

.etrans {
  -webkit-transition: all 0.2s ease-out;
  -moz-transition: all 0.2s ease-out;
  -ms-transition: all 0.2s ease-out;
  -o-transition: all 0.2s ease-out;
  transition: all 0.2s ease-out;
}
</style>
