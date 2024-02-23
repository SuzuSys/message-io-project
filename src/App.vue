<script setup lang="ts">
import { ref } from 'vue';
import { useAxios } from '@vueuse/integrations/useAxios';
import ChannelFrame from './components/ChannelFrame.vue';
import { Channel, IncompleteChannel } from './types/response';

interface requestData {
  channel_id: number | null;
  next_message_id: number | null;
  limit: number | null;
}

const url = 'https://fqrkuiesr2pmebwkgvy7qczw3e0ljzse.lambda-url.us-east-1.on.aws/';
const { execute } = useAxios(url, { method: 'POST' }, { immediate: false });

const urlParams = new URLSearchParams(window.location.search);
const channel_id: any = urlParams.get('channel_id');
const limit: any = urlParams.get('limit');
const requestData: requestData = {
  channel_id: (typeof channel_id) === 'number' ? channel_id : null,
  next_message_id: null,
  limit: (typeof limit) === 'number' ? limit : null,
}

const channels = ref<Array<Channel>>([]);
const incompleteChannelsId = ref<Array<number>>([]);
getResponse();

async function getResponse() {
  try {
    const result = await execute({ data: requestData });
    const response = result.response.value;
    if (!response) {
      console.log(result.response);
      return;
    }
    const responseData: Array<Channel|IncompleteChannel> = response.data;
    responseData.forEach(el => {
      if ('name' in el) {
        channels.value.push(el);
      } else {
        incompleteChannelsId.value.push(el.id);
      }
    });
    console.log(channels)
  } catch (e) {
    console.log(e);
  }
}

</script>

<template>
  <div>
    <channel-frame 
      v-for="(c, index) in channels" 
      :key="index"
      :guild_name="c.guild.name"
      :category="c.category"
      :channel_name="c.name"
      :messages="c.messages"
    />
  </div>
</template>

<style scoped>
</style>
