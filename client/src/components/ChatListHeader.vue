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
import ChatCard from "./ChatCard.vue";
  
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
			this.$emit("switch", userId);
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

/* Adjusting the chat card container */
.chat-list-header > div {
  max-height: 300px; /* Set a max height */
  overflow-y: auto; /* Allow scrolling for overflow */
}

/* Custom scrollbar styles */
.chat-list-header > div::-webkit-scrollbar {
  width: 8px;
}

.chat-list-header > div::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.chat-list-header > div::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1);
}

/* Spacing between chat cards */
.chat-list-header > div > ChatCard {
  margin-bottom: 10px;
}

.chat-list-header > div > ChatCard:last-child {
  margin-bottom: 0; /* Remove margin for the last item */
}
</style>
  