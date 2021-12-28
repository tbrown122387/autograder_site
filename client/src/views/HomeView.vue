<template>
  <v-container>
    <v-col>
      <v-card elevation="2">
        <v-card-title> Autograding Bundler</v-card-title>
        <v-card-text>
          <p>
            This site helps you make "bundles" for autograding. Currently, we
            support the following:
          </p>
          <ul>
            <li>Autograding in Gradescope with R</li>
          </ul>
          <br />
          <p>These are some more features we have planned:</p>
          <ul>
            <li>Autograding in Gradescope with Python</li>
            <li>Autograding in Gradescope with Python via OtterGrader</li>
            <li>Autograding Locally with R</li>
          </ul>
        </v-card-text>
      </v-card>
    </v-col>
  </v-container>
</template>

<script>
export default {
  name: "HomeView",
};
</script>
