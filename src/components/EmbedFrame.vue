<script setup lang="ts">
import { Message } from '../types/response';
interface EmbedProps {
  embeds: Message['embeds'];
}
const p = defineProps<EmbedProps>();
</script>
<template>
  <div v-for="(embed, index) in p.embeds" :key="index">
    <v-card variant="flat" class="my-2">
      {{ embed }}
    </v-card>
  </div>
</template>
