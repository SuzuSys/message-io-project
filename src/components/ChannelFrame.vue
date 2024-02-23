<script setup lang="ts">
import { reactive } from 'vue';
import { Message } from '../types/response';
interface Props {
  guild_name: string;
  category: null | {
    id: number;
    name: string;
  };
  channel_name: string;
  messages: Array<Message>;
}
interface State {
  title: string;
}
const props = defineProps<Props>();
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
      variant="outlined"
    >
      
    </v-card>
  </div>
</template>