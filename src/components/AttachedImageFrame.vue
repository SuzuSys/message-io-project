<script setup lang="ts">
interface AttachedImageProps {
  urls: Array<string>;
}
const p = defineProps<AttachedImageProps>();
</script>
<template>
  <div v-for="(url, index) in p.urls" :key="index">
    <v-card variant="flat" class="my-2">
      <v-img :src="url" max-width="200px" max-height="200px"></v-img>
    </v-card>
  </div>
</template>
