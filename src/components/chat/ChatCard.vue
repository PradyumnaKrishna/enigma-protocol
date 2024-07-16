<template>
  <button
    class="rounded-xl bg-neutral-900 hover:pointer border text-center p-4 w-full color-gray-400 transition duration-300"
    :class="[isActive ? 'border-blue-500' : 'border-gray-600']"
    @click="$emit('switch')"
  >
    {{ userId }}
  </button>
</template>

<script>
export default {
  name: 'ChatCard',
  props: {
    userId: String,
    isActive: Boolean,
  },
}
</script>
