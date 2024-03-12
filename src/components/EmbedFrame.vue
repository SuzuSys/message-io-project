<script setup lang="ts">
import { ref } from 'vue';
import { Message } from '../types/response';
interface EmbedProps {
  embeds: Message['embeds'];
}
const p = defineProps<EmbedProps>();
type CleanedEnbed =
  | {
      type: 'image' | 'gifv';
      thumbnail: {
        url: string;
        width: null | number;
        height: null | number;
      };
    }
  | {
      type: 'video';
      url: string;
    }
  | {
      type: 'link';
      thumbnail: null | {
        url: string;
        width: null | number;
        height: null | number;
      };
      title: string;
      description: null | string;
    };
const cleanedEnbeds = ref<CleanedEnbed[]>([]);
p.embeds.forEach((embed) => {
  switch (embed.type) {
    case 'rich':
      break;
    case 'image':
    case 'gifv':
      if (embed.thumbnail && embed.thumbnail.url) {
        cleanedEnbeds.value.push(embed as CleanedEnbed);
        console.log(embed);
      }
      break;
    case 'video':
      if (embed.url) {
        console.log(embed);
        cleanedEnbeds.value.push(embed as CleanedEnbed);
      }
      break;
    case 'article':
      console.log(embed);
      break;
    case 'link':
      if (embed.title) {
        cleanedEnbeds.value.push(embed as CleanedEnbed);
      }
      break;
  }
});
function adjustMaxHeight(height: number | null) {
  if (height && height < 200) {
    return height;
  } else {
    return 200;
  }
}
</script>
<template>
  <div v-for="(embed, index) in cleanedEnbeds" :key="index">
    <v-card
      v-if="embed.type === 'image' || embed.type === 'gifv'"
      variant="flat"
      class="my-2"
    >
      <v-img
        :src="embed.thumbnail.url"
        :max-height="adjustMaxHeight(embed.thumbnail.height)"
        position="left"
      />
    </v-card>
    <v-card v-else-if="embed.type === 'video'" variant="flat" class="my-2">
      <video
        controls
        :src="embed.url"
        :style="{
          maxHeight: '200px',
        }"
      ></video>
    </v-card>
    <v-card v-else-if="embed.type === 'link'" variant="flat" class="my-2">
      {{ embed }}
    </v-card>
  </div>
</template>
