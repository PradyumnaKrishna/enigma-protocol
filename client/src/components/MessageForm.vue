<template>
  <form class="message_form" v-on:submit.prevent="onSubmit">
    <input type="text" v-model="text" placeholder="Type a message..." class="message_input"
      v-bind:class="{ message_input_focused: isFocused }" @focus="isFocused = true" @blur="isFocused = false" />

    <button type="submit" class="send_button">
      <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path d="M2.00098 21.1719L21.001 12.1729L2.00098 3.17188V10.1719L17.001 12.1729L2.00098 14.1729V21.1719Z"
          fill="white" />
      </svg>
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
      isFocused: false
    }
  },

  methods: {
    onSubmit() {
      const text = this.text.trim();
      if (text.trim() === '') {
        return;
      }

      this.$emit('sendMessage', text);
      this.text = '';
    },
  },
})

</script>

<style scoped>
.message_form {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 68px;
  margin-left: 12px;
  margin-right: 12px;
  width: calc(100% - 12px - 12px);
  margin-bottom: 0px;
}

.message_input {
  margin-right: 10px;
  width: calc(100% - 16px - 16px - 36px - 4px);
  outline: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background-color: #333333;
  color: white;
  font-size: 14px;
  letter-spacing: 0.17px;
  padding: 0px 15px;
  height: 36px;
  border-radius: 8px;
  transition: border .44s ease;
}

.message_input_focused {
  border: 1px solid dodgerblue;
}

.send_button {
  cursor: pointer;
  background-color: dodgerblue;
  border: 1px solid dodgerblue;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  color: white;
  transition: all .44s ease;
}
</style>
