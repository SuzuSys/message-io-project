<script setup lang="ts">
import { ref } from 'vue';
import ContentFrame from './ContentFrame.vue';
import ReactionFrame from './ReactionFrame.vue'
import { Message } from '../types/response';
interface MessageProps {
  message: Message;
};
const props = defineProps<MessageProps>();
const authorNameColor = ref<string>('#ffffff');
/*
if (props.message.author.roles && props.message.author.roles.length > 0) {
  authorNameColor.value = props.message.author.roles[0].color;
  console.log(props.message.author.roles)
}
*/
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
          <div :style="{ color: authorNameColor }">
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
      <div v-if="props.message.reactions.length > 0" class="ma-3">
        <reaction-frame
          :emoji="props.message.reactions" 
        />
      </div>
    </v-card-text>
  </v-card>
</template>