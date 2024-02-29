<script setup lang="ts">
import ContentFrame from './ContentFrame.vue';
import { Message } from '../types/response';
interface MessageProps {
  message: Message;
};
const props = defineProps<MessageProps>();

</script>
<template>
  <v-card
    class="mx-auto my-2"
    rounded="0"
    variant="text"
  >
    <v-card-text>
      <v-row>
        <v-col class="flex-grow-0 flex-shrink-0">
          <v-avatar 
            style="width: 36px; height: 36px"
            :image="props.message.author.display_avatar.url" 
          />
        </v-col>
        <v-col
          class="flex-grow-1 flex-shrink-0"
        >
          {{ props.message.author.nick ? props.message.author.nick : props.message.author.display_name }}
          <br>
          <span class="text-disabled">{{ props.message.created_at }}</span>
          <span class="text-disabled" v-if="props.message.edited_at">
            ( edited at {{ props.message.edited_at }} )
          </span>
        </v-col>
      </v-row>
      <v-row class="px-5">
        <content-frame 
          :content="props.message.content" 
          :except="[]"
          :mention="props.message" />
      </v-row>
    </v-card-text>
  </v-card>
</template>