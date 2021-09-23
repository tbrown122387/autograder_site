<template>
  <v-card elevation="2">
    <v-card-title>API Database Create Example</v-card-title>
    <v-card-text>
      <v-text-field label="Title" color="teal" v-model="commentTitle">
      </v-text-field>
      <v-text-field label="Write a comment" color="teal" v-model="commentText">
      </v-text-field>
    </v-card-text>

    <v-card-actions>
      <v-btn text color="teal" @click="submitComment">Submit Comment</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  data: () => {
    return {
      text: false,
      commentTitle: "",
      commentText: "",
    };
  },
  methods: {
    ...mapActions("General", ["setComments"]),
    async submitComment() {
      const response = await axios.post(
        process.env.VUE_APP_API_ENDPOINT + "/comments/create",
        {
          title: this.commentTitle,
          text: this.commentText,
        }
      );

      console.log(response);
      this.setComments();
    },
  },
};
</script>

<style>
</style>