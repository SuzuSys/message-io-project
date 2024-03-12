<script setup lang="ts">
import { Message } from '../types/response';
import ContentFrame from './ContentFrame.vue';
import { ListStruct } from '../types/content';
interface ListProps {
  li: Array<ListStruct>;
  mention: {
    mentions: Message['mentions'];
    channel_mentions: Message['channel_mentions'];
    role_mentions: Message['role_mentions'];
  };
}
const props = defineProps<ListProps>();
</script>
<template>
  <ol
    v-if="props.li[0].firstNumber"
    :start="props.li[0].firstNumber"
    :style="{
      marginLeft: props.li[0].firstNumber.toString().length * 8 + 10 + 'px',
    }"
  >
    <li v-for="(li, index) in props.li" :key="index">
      <content-frame
        :content="li.content"
        :except="[]"
        :mention="props.mention"
      />
      <list-frame v-if="li.child" :li="li.child" :mention="props.mention" />
    </li>
  </ol>
  <ul v-else :style="{ marginLeft: '20px' }">
    <li v-for="(li, index) in props.li" :key="index">
      <content-frame
        :content="li.content"
        :except="[]"
        :mention="props.mention"
      />
      <list-frame v-if="li.child" :li="li.child" :mention="props.mention" />
    </li>
  </ul>
</template>
