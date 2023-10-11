<template>
  <div>
    <p id="userId" class="inputBox">
      User ID :
      <strong @click="copy(user)" title="click to copy">{{ user }}</strong>
    </p>
    <ToastMessage :toastmsg="toastmsg" :toastType="toastType" />
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
import ToastMessage from "../components/ToastMessage.vue";
export default {
  name: "UserInfo",
  components: {
    ToastMessage
  },
  props: {
    user: String,
    toastmsg: String,
    toastType: String,
  },
  data() {
    return {
      room: "",
    };
  },
  methods: {
    copy(userId) {
    // Emit the event to parent component to handle the copy action
    this.$emit('requestCopy', userId);
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
/* Styles related to UserInfo component can be added here */
</style>
