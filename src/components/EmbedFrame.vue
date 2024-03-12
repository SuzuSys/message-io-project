<script setup lang="ts">
import { Message } from '../types/response';
interface EmbedProps {
  embeds: Message['embeds'];
}
const p = defineProps<EmbedProps>();
</script>
<template>
  <!--
    <div v-for="(embed, index) in p.embeds" :key="index">
    <v-card variant="flat" class="my-2">
      <v-img :src="url" max-width="200px" max-height="200px"></v-img>
    </v-card>
  </div>
  -->
</template>
