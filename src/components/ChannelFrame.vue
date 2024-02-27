<script setup lang="ts">
import { reactive } from 'vue';
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
interface State {
  title: string;
}
const props = defineProps<ChannelProps>();
const state: State = reactive<State> ({
  title: '',
})

state.title = props.guild_name + ' > ';
if (props.category) {
  state.title += props.category.name + ' > ';
}
state.title += props.channel_name
</script>
<template>
  <div>
    <v-card
      class="mx-auto"
      max-width="800"
      :title="state.title"
    >
      <message-frame
        v-for="m in props.messages"
        :key="m.id"
        :message="m"
      />
    </v-card>
  </div>
</template>