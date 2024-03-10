<script setup lang="ts">
import { Message } from '../types/response';
interface AttachmentProps {
  attachments: Message['attachments'];
}
const p = defineProps<AttachmentProps>();
type category = 'image' | 'audio' | 'video' | 'other';

function getCategory(content_type: string | null): category {
  if (!content_type) {
    return 'other';
  } else if (/image/.test(content_type)) {
    return 'image';
  } else if (/audio/.test(content_type)) {
    return 'audio';
  } else if (/video/.test(content_type)) {
    return 'video';
  } else {
    return 'other';
  }
}
</script>
<template>
  <div v-for="attachment in p.attachments" :key="attachment.id">
    <v-card
      v-if="getCategory(attachment.content_type) === 'other'"
      prepend-icon="mdi-file-outline"
      :href="attachment.url"
      :title="attachment.filename"
      variant="outlined"
      class="my-2"
    ></v-card>
    <v-card
      v-else-if="getCategory(attachment.content_type) === 'image'"
      variant="flat"
      class="my-2"
    >
      <v-img :src="attachment.url" max-width="200px" max-height="200px"></v-img>
    </v-card>
    <v-card
      v-else-if="getCategory(attachment.content_type) === 'audio'"
      class="audio-card my-2"
    >
      <v-card-text class="text-h6">{{ attachment.filename }}</v-card-text>
      <audio controls :src="attachment.url"></audio>
    </v-card>
    <v-card
      v-else-if="getCategory(attachment.content_type) === 'video'"
      class="my-2"
    >
      <video controls :src="attachment.url"></video>
    </v-card>
  </div>
</template>
<style scoped>
.audio-card {
  border: 2px solid gray;
  padding: 5px;
}
video {
  width: 100%;
  display: block;
}
</style>
