<script setup lang="ts">
import { ref } from 'vue';
import { Message } from '../types/response';
interface ReactionProps {
  emoji: Message['reactions'];
}
const p = defineProps<ReactionProps>();
interface State {
  menu: Array<boolean>;
}
const state = ref<State>({
  menu: Array(p.emoji.length).fill(false),
});

function NameColor(
  top_role: Message['reactions'][0]['users'][0]['top_role']
): string {
  if (top_role && top_role.color !== '#000000') {
    return top_role.color;
  }
  return '#ffffff';
}
</script>
<template>
  <div>
    <v-menu
      v-model="state.menu[index]"
      location="bottom start"
      origin="top start"
      transition="scale-transition"
      v-for="(reaction, index) in p.emoji"
      :key="index"
    >
      <template v-slot:activator="{ props }">
        <v-chip v-bind="props" class="ma-2" density="comfortable" label>
          <v-img
            v-if="typeof reaction.emoji_obj === 'object'"
            :src="reaction.emoji_obj.url"
            width="1em"
            class="mr-2"
          />
          <span v-else class="mr-1">{{ reaction.emoji_obj }}</span>
          <span>{{ reaction.count }}</span>
        </v-chip>
      </template>
      <v-card width="300">
        <v-card-text>
          <v-row v-for="user in reaction.users" :key="user.id">
            <v-col class="flex-grow-0 flex-shrink-0 pa-1">
              <v-avatar
                style="width: 1.5em; height: 1.5em"
                :image="user.display_avatar.url"
              />
            </v-col>
            <v-col class="flex-grow-1 flex-shrink-0 my-auto pa-1">
              <div :style="{ color: NameColor(user.top_role) }">
                {{ user.nick ? user.nick : user.display_name }}
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-menu>
  </div>
</template>
