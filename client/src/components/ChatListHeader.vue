<template>
    <div class="chat-list-header">
      <h3>Chats</h3>
      <div>
        <ChatCard
          v-for="user in users"
          :key="user"
          :userId="user"
          :isActive="activeUser === user"
          @switch="switchChat(user)"
        />
      </div>
    </div>
  </template>
  
  <script>
  import ChatCard from './ChatCard.vue';
  
  export default {
    name: "ChatListHeader",
    components: {
      ChatCard
    },
    props: {
      users: {
        type: Array,
        required: true
      },
      activeUser: {
        type: String,
        default: null
      }
    },
    methods: {
      switchChat(userId) {
        this.$emit('switch', userId);
      }
    }
  };
  </script>
  
  <style scoped>
  .chat-list-header {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 10px 15px; 
  border-radius: 10px; 
  margin-bottom: 20px; 
}

.chat-list-header h3 {
  color: #f9f6f7; 
  font-size: 1.2em; 
  margin-bottom: 15px; 
}

.chat-list-header ul {
  max-height: 300px; 
  overflow-y: auto;
}

/* Custom scrollbar styles */
.chat-list-header ul::-webkit-scrollbar {
  width: 8px;
}

.chat-list-header ul::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.chat-list-header ul::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1);
}

.chat-list-header li {
  margin-bottom: 10px;
}

.chat-list-header li:last-child {
  margin-bottom: 0;
}

  </style>
  