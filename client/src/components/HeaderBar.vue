<template>
  <!-- This example requires Tailwind CSS v2.0+ -->
  <nav class="py-4 bg-green-700">
    <div class="items-center justify-between md:flex">
      <div class="gap-1 md:space-x-4 md:ml-6 md:flex">
        <div class="px-3 py-2 text-xl font-bold text-white">Autograding Bundler</div>
        <router-link :to="{ name: 'Home' }" class="router-link"> Home </router-link>

        <router-link :to="{ name: 'Grading' }" class="router-link">R Grading </router-link>
      </div>
      <div v-if="isLoggedIn" class="md:mr-6 md:flex">
        <router-link class="router-link" :to="{ name: 'Account' }"> Account </router-link>
      </div>
      <div v-else class="md:mr-6 md:flex">
        <router-link class="router-link" :to="{ name: 'Login' }"> Login </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  methods: {
    ...mapActions("AuthModule", [""]),
  },
  computed: {
    ...mapState("AuthModule", ["isLoggedIn"]),
  },
};
</script>

<style>
.router-link {
  @apply flex items-center px-3 py-2 text-white bg-green-800 rounded-md  hover:bg-green-600 focus:outline-none focus:ring-1 focus:ring-white;
}

.router-link-active {
  @apply border-2 md:border-0 md:border-b-4  rounded-none rounded-t-md bg-green-900 focus:outline-none focus:ring-1 focus:ring-white;
}
</style>