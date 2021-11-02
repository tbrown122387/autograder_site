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
    <v-col>
      <v-card elevation="2">
        <MonacoEditor
          class="editor"
          theme="vs-dark"
          v-model="code1"
          language="python"
        />
      </v-card>
    </v-col>
    <v-col>
      <v-card elevation="2">
        <MonacoEditor class="editor" v-model="code2" language="python" />
      </v-card>
    </v-col>
    <v-col>
      <v-card elevation="2">
        <MonacoEditor class="editor" v-model="code3" language="python" />
      </v-card>
    </v-col>
    <v-col>
      <v-menu transition="slide-y-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" class="ma-2" v-bind="attrs" v-on="on">
            Slide Y Transition
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="n in 5" :key="n" link>
            <v-list-item-title v-text="'Item ' + n"></v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-col>
  </v-container>
</template>

<script>
import MonacoEditor from "vue-monaco";

export default {
  name: "Home",
  components: {
    MonacoEditor,
  },

  data() {
    return {
      code1: "x = [1,2,3]",
      code2: "y = 'Hello World'",
      code3: "z = 3",
    };
  },
};
</script>
<style>
.editor {
  height: 100px;
}
</style>
