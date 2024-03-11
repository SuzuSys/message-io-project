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
const emit = defineEmits<{
  pushAttachedImage: [url: string];
}>();
const pushAttachedImage = (url: string) => {
  emit('pushAttachedImage', url);
};
</script>
<template>
  <ol
    v-if="props.li[0].first_number"
    :start="props.li[0].first_number"
    :style="{
      marginLeft: props.li[0].first_number.toString().length * 8 + 10 + 'px',
    }"
  >
    <li v-for="(li, index) in props.li" :key="index">
      <content-frame
        :content="li.content"
        :except="[]"
        :mention="props.mention"
        @push-attached-image="pushAttachedImage"
      />
      <list-frame
        v-if="li.child"
        :li="li.child"
        :mention="props.mention"
        @push-attached-image="pushAttachedImage"
      />
    </li>
  </ol>
  <ul v-else :style="{ marginLeft: '20px' }">
    <li v-for="(li, index) in props.li" :key="index">
      <content-frame
        :content="li.content"
        :except="[]"
        :mention="props.mention"
        @push-attached-image="pushAttachedImage"
      />
      <list-frame
        v-if="li.child"
        :li="li.child"
        :mention="props.mention"
        @push-attached-image="pushAttachedImage"
      />
    </li>
  </ul>
</template>
