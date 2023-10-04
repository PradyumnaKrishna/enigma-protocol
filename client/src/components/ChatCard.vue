<template>
  <div class="card-body contacts_body">
    <div class="contacts">
      <button
          class="contact_body etrans"
          :style="
            isActive
            ? { 'background-color': 'rgba(255,255,255,0.1)' }
            : null
          "
          @click="$emit('switch')"
      >
        {{ userId }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "ChatCard",
  props: {
    userId: String,
    isActive: Boolean
  },
}
</script>

<style scoped>
.contact_body {
  border-radius: 15px !important;
  border: 1px double rgba(0, 0, 0, 0.3) !important;
  background-color: rgba(55, 55, 55, 0.1);
  text-align: center;
  padding: 1rem;
  width: 100%;
  color: #f9f6f7;
}

.etrans {
  -webkit-transition: all 0.2s ease-out;
  -moz-transition: all 0.2s ease-out;
  -ms-transition: all 0.2s ease-out;
  -o-transition: all 0.2s ease-out;
  transition: all 0.2s ease-out;
}
</style>
