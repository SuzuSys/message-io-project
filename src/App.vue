<script setup lang="ts">
let urlParams = new URLSearchParams(window.location.search);
console.log(urlParams.has('message_id')); // true
console.log(urlParams.get('message_id')); // "MyParam"
</script>

<template>
  <div>
    <v-btn>
      Button
    </v-btn>
  </div>
</template>

<style scoped>
</style>
