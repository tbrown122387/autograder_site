<template>
  <v-app>
    <v-card elevation="2" flat>
      <HeaderBar />
    </v-card>

    <!-- Sizes your content based upon application components -->
    <v-main>
      <!-- Provides the application the proper gutter -->
      <v-container fluid>
        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
import HeaderBar from "./components/HeaderBar.vue";
export default {
  name: "App",
  components: {
    HeaderBar,
  },
  data() {
    return {};
  },
};
</script>
