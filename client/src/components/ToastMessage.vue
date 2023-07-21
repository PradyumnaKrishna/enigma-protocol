<template>
  <div
    v-if="toastmsg"
    class="toast-error"
    :style="{
      backgroundColor: toastType === `error` ? '#d32f2f' : '#0288d1',
    }"
  >
    {{ toastmsg }}
  </div>
</template>

<script>
export default {
  props: {
    toastmsg: {
      type: String,
      required: true,
    },
    toastType: {
      type: String,
      required: true,
    },
  },
};
</script>

<style>
/* Toast message */
.toast-error {
  visibility: visible;
  min-width: 250px;
  height: fit-content;
  margin-left: -125px;
  background-color: #333;
  color: #fff;
  text-align: center;
  border-radius: 2px;
  padding: 16px;
  position: fixed;
  z-index: 1;
  left: 50%;
  top: 30px;
  -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
  animation: fadein 0.5s, fadeout 0.5s 2.5s;
}

/* Animations to fade the toast in and out */
@-webkit-keyframes fadein {
  from {
    bottom: 0;
    opacity: 0;
  }
  to {
    bottom: 30px;
    opacity: 1;
  }
}

@keyframes fadein {
  from {
    bottom: 0;
    opacity: 0;
  }
  to {
    bottom: 30px;
    opacity: 1;
  }
}

@-webkit-keyframes fadeout {
  from {
    bottom: 30px;
    opacity: 1;
  }
  to {
    bottom: 0;
    opacity: 0;
  }
}

@keyframes fadeout {
  from {
    bottom: 30px;
    opacity: 1;
  }
  to {
    bottom: 0;
    opacity: 0;
  }
}
</style>
