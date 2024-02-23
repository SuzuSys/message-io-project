<script setup lang="ts">
import { ref } from 'vue';
import { useAxios } from '@vueuse/integrations/useAxios';
import ChannelFrame from './components/ChannelFrame.vue';
import { Channel, IncompleteChannel } from './types/response';

interface requestData {
  channel_id: string | null;
  next_message_id: string | null;
  limit: number | null;
}

const url = 'https://fqrkuiesr2pmebwkgvy7qczw3e0ljzse.lambda-url.us-east-1.on.aws/';
const { execute } = useAxios(url, { method: 'POST' }, { immediate: false });

const urlParams = new URLSearchParams(window.location.search);
const requestData: requestData = {
  channel_id: getIntegerParam('channel_id'),
  next_message_id: null,
  limit: getParamConvertNumber('limit')
}
console.log(requestData);

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

function getIntegerParam(paramName: string) {
  const paramStr = urlParams.get(paramName);
  const re = /^\d+$/;
  if (paramStr && re.test(paramStr)) return paramStr
  return null;
}

function getParamConvertNumber(paramName: string) {
  const result = getIntegerParam(paramName);
  if (result) return parseInt(result);
  return null;
}
</script>

<template>
  <div>
    <channel-frame 
      v-for="c in channels" 
      :key="c.id"
      :guild_name="c.guild.name"
      :category="c.category"
      :channel_name="c.name"
      :messages="c.messages"
    />
  </div>
</template>

<style scoped>
</style>
