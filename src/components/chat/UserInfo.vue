<template>
  <div class="p-2">
    <p id="userId" class="inputBox">
      User ID : <strong @click="copy(user)">{{ user }}</strong>
    </p>
    <form v-on:submit.prevent="onSubmit" class="form">
      <div class="inline-flex gap-2 items-center w-full">
        <input
          type="text"
          v-model="room"
          placeholder="Other User's ID"
          class="bg-neutral-900 rounded-lg outline-none border border-gray-600 text-gray-400 placeholder:text-gray-500 focus:border-blue-600 transition-all duration-300 w-full h-10 p-2"
          required
        />
        <button class="text-gray-500 w-6" type="submit">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="16" />
            <line x1="8" y1="12" x2="16" y2="12" />
          </svg>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'UserInfo',
  props: {
    user: String,
  },
  data() {
    return {
      room: '',
    }
  },
  methods: {
    copy(userId) {
      // Emit the event to parent component to handle the copy action
      this.$emit('requestCopy', userId)
    },
    // joinRoom() {
    //   // Submit the form
    // },
    onSubmit() {
      // If the form is submitted, trigger the join room logic
      this.$emit('joinRoom', this.room)
    },
  },
}
</script>
