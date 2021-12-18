.<template>
  <v-app-bar color="teal" dark>
    <v-container>
      <v-app-bar-title>Autograding Bundler</v-app-bar-title>
    </v-container>

    <v-tabs class="m9-nl" right background-color="teal" dark>
      <v-tab color="white" to="/">Home</v-tab>
      <v-tab color="white" to="/grading">Grading in R</v-tab>
      <v-tab color="white" to="/login">Login</v-tab>
    </v-tabs>
  </v-app-bar>
</template>

<script>
export default {
  name: "HeaderBar",
};
</script>

<style>
</style>