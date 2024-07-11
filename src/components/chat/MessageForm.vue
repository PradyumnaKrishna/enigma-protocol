<template>
  <form class="inline-flex gap-2 w-full p-2" v-on:submit.prevent="onSubmit">
    <input
      type="text"
      v-model="text"
      placeholder="Type a message..."
      class="bg-neutral-900 rounded-lg outline-none border border-gray-600 text-gray-400 placeholder:text-gray-500 focus:border-blue-600 transition-all duration-300 w-full h-10 p-2"
    />

    <button type="submit" class="h-10 w-10 bg-blue-600 text-white rounded-lg cursor-pointer">
      <span class="w-6 mx-auto block">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M2.00098 21.1719L21.001 12.1729L2.00098 3.17188V10.1719L17.001 12.1729L2.00098 14.1729V21.1719Z"
            fill="currentColor"
          />
        </svg>
      </span>
    </button>
  </form>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MessageForm',
  data() {
    return {
      text: '',
    }
  },

  methods: {
    onSubmit() {
      const text = this.text.trim()
      if (text.trim() === '') {
        return
      }

      this.$emit('sendMessage', text)
      this.text = ''
    },
  },
})
</script>
