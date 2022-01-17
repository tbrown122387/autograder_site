<template>
  <div>
    <header-bar />
    <router-view v-slot="{ Component }">
      <!-- <transition> -->
      <component :is="Component" />
      <!-- </transition> -->
    </router-view>
  </div>
</template>

<script>
import HeaderBar from "./components/HeaderBar.vue";
export default {
  components: {
    HeaderBar,
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
input.textbox {
  @apply w-full px-4 py-2 text-gray-700 transition duration-200 rounded  focus:border-green-800 focus:ring-green-800;
}

input.checkbox {
  @apply text-green-800 rounded cursor-pointer focus:ring-green-800 w-5 h-5 hover:ring-2 hover:ring-green-800 hover:ring-offset-2 hover:ring-offset-white;
}

input.error {
  @apply text-red-500 focus:border-red-500 border-red-500 focus:ring-red-500;
}

.blue-button {
  @apply text-white transition duration-100 bg-blue-700 rounded shadow focus:outline-none hover:bg-blue-600 hover:ring-2 focus:ring-2 hover:ring-offset-white hover:ring-offset-2 hover:ring-blue-600 focus:ring-offset-white focus:ring-offset-2 focus:ring-blue-600;
}

.red-button {
  @apply text-white transition duration-100 bg-red-700 rounded shadow focus:outline-none hover:bg-red-600 hover:ring-2 focus:ring-2 hover:ring-offset-white hover:ring-offset-2 hover:ring-red-600 focus:ring-offset-white focus:ring-offset-2 focus:ring-red-600;
}

.green-button {
  @apply text-white transition duration-100 bg-green-700 rounded shadow focus:outline-none hover:bg-green-600 hover:ring-2 focus:ring-2 hover:ring-offset-white hover:ring-offset-2 hover:ring-green-600 focus:ring-offset-white focus:ring-offset-2 focus:ring-green-600;
}
</style>
