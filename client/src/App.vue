<template>
  <!-- App.vue -->

  <v-app>
    <v-card elevation="2" flat>
      <v-app-bar color="teal" dark>
        <v-container>
          <v-app-bar-title>Autograding Bundler</v-app-bar-title>
        </v-container>

        <v-tabs class="m9-nl" right background-color="teal" dark>
          <v-tab color="white" to="/">Home</v-tab>
          <v-tab color="white" to="/about">About</v-tab>
          <v-tab color="white" to="/grading">Grading in R</v-tab>
        </v-tabs>
      </v-app-bar>
    </v-card>

    <!-- Sizes your content based upon application components -->
    <v-main width="1200px">
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
export default {
  name: "App",
  data() {
    return {};
  },
};
</script>