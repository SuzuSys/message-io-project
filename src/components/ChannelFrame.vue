<script setup lang="ts">
import MessageFrame from './MessageFrame.vue';
import { Message } from '../types/response';
interface ChannelProps {
  guild_name: string;
  category: null | {
    id: string;
    name: string;
  };
  channel_name: string;
  messages: Array<Message>;
}
const props = defineProps<ChannelProps>();
</script>
<template>
  <v-card class="mx-auto" max-width="800">
    <v-card-title>
      {{ props.guild_name }}
      <span class="text-disabled">> </span>
      <span v-if="props.category">
        {{ props.category.name }}
        <span class="text-disabled"> ></span>
      </span>
      {{ props.channel_name }}
    </v-card-title>
    <message-frame v-for="m in props.messages" :key="m.id" :message="m" />
  </v-card>
</template>
