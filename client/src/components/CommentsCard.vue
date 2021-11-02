<template>
  <v-container>
    <v-row class="d-flex" v-if="comments.length">
      <v-card
        class="ma-2"
        elevation="2"
        v-for="(comment, index) in comments"
        :key="index"
      >
        <v-card-title>{{ comment.title }}</v-card-title>
        <v-card-text> {{ comment.text }} </v-card-text>

        <v-card-actions>
          <v-btn text color="teal" @click="deleteComment(comment.id)">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <v-row v-else>
      <v-card-title>No Comments Yet </v-card-title>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import axios from "axios";

export default {
  data() {
    return {
      timeout: null,
    };
  },
  computed: {
    ...mapState("General", ["comments"]),
  },
  methods: {
    ...mapActions("General", ["setComments"]),
    async deleteComment(id) {
      const response = await axios.post(
        process.env.VUE_APP_API_ENDPOINT + "/comments/delete",
        {
          id: id,
        }
      );
      console.log(response);
      this.setComments();
    },
  },
  created() {
    this.timeout = setInterval(this.setComments, 3000); // calls setComments action every 3 seconds
  },
  destroyed() {
    clearTimeout(this.timeout);
  },
};
</script>

<style>
</style>