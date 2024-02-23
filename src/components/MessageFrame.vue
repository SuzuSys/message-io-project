<script setup lang="ts">
import { Message } from '../types/response';
interface MessageProps {
  message: Message;
}
const props = defineProps<MessageProps>();
</script>

<template>
  <div>
    <v-card
      class="mx-auto"
      :subtitle="props.message.created_at"
      rounded="0"
    >
      <template v-slot:title class="text-h5">
        <div class="text-subtitle-1">
          {{ props.message.author.display_name }}
        </div>
      </template>
      <template v-slot:prepend>
        <v-avatar size="32" class="mr-5">
          <v-img
            class="rounded-circle"
            :src="props.message.author.display_avatar.url"
            alt="avatar"
          ></v-img>
        </v-avatar>
      </template>
      <v-card-text>
        {{ props.message.content }}
      </v-card-text>
    </v-card>
  </div>
</template>