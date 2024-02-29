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
          <div>
            {{ props.message.author.nick ? props.message.author.nick : props.message.author.display_name }}
          </div>
          <div>
            <div class="text-disabled d-inline-flex">{{ props.message.created_at }}&emsp;</div>
            <div class="text-disabled d-inline-flex" v-if="props.message.edited_at">( edited at {{ props.message.edited_at }} )</div>
          </div>
        </v-col>
      </v-row>
      <div class="ma-3">
        <content-frame 
          :content="props.message.content" 
          :except="[]"
          :mention="props.message" />
      </div>
    </v-card-text>
  </v-card>
</template>