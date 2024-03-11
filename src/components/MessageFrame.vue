<script setup lang="ts">
import { ref } from 'vue';
import ContentFrame from './ContentFrame.vue';
import ReactionFrame from './ReactionFrame.vue';
import AttachmentFrame from './AttachmentFrame.vue';
import AttachedImageFrame from './AttachedImageFrame.vue';
import { Message } from '../types/response';
interface MessageProps {
  message: Message;
}
const props = defineProps<MessageProps>();
const authorNameColor = ref<string>('#ffffff');
if (
  props.message.author.top_role &&
  props.message.author.top_role.color !== '#000000'
) {
  authorNameColor.value = props.message.author.top_role.color;
}
const attachedImages = ref<Array<string>>([]);
const pushAttachedImage = (url: string) => {
  attachedImages.value.push(url);
};
</script>
<template>
  <v-card class="mx-auto my-2" rounded="0" variant="text">
    <v-card-text>
      <v-row>
        <v-col class="flex-grow-0 flex-shrink-0">
          <v-avatar
            style="width: 36px; height: 36px"
            :image="props.message.author.display_avatar.url"
          />
        </v-col>
        <v-col class="flex-grow-1 flex-shrink-0">
          <div :style="{ color: authorNameColor }">
            {{
              props.message.author.nick
                ? props.message.author.nick
                : props.message.author.display_name
            }}
          </div>
          <div>
            <div class="text-disabled d-inline-flex">
              {{ props.message.created_at }}&emsp;
            </div>
            <div
              class="text-disabled d-inline-flex"
              v-if="props.message.edited_at"
            >
              ( edited at {{ props.message.edited_at }} )
            </div>
          </div>
        </v-col>
      </v-row>
      <div class="ma-3">
        <content-frame
          :content="props.message.content"
          :except="[]"
          :mention="props.message"
          @push-attached-image="pushAttachedImage"
        />
      </div>
      <div v-if="props.message.reactions.length > 0" class="ma-3">
        <reaction-frame :emoji="props.message.reactions" />
      </div>
      <div v-if="props.message.attachments.length > 0" class="ma-3">
        <attachment-frame :attachments="props.message.attachments" />
      </div>
      <div v-if="attachedImages.length > 0">
        <attached-image-frame :urls="attachedImages" />
      </div>
    </v-card-text>
  </v-card>
</template>
