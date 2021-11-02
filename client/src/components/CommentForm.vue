<template>
  <v-form
    v-model="valid"
    @submit.prevent="submitComment"
    id="gradingForm"
    ref="form"
  >
    <v-card elevation="2">
      <v-card-title>API Database Create Example</v-card-title>
      <v-card-text>
        <v-text-field
          label="Title"
          color="teal"
          v-model="commentTitle"
          :rules="existsRule"
        >
        </v-text-field>
        <v-text-field
          label="Write a comment"
          color="teal"
          v-model="commentText"
          :rules="existsRule"
        >
        </v-text-field>
      </v-card-text>

      <v-card-actions>
        <v-btn
          type="submit"
          form="gradingForm"
          color="teal"
          text
          @submit="submitComment"
        >
          Submit Comment
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  data: () => {
    return {
      text: false,
      valid: false,
      commentTitle: "",
      commentText: "",
      existsRule: [(v) => !!v || "This field is required"],
    };
  },
  methods: {
    ...mapActions("General", ["setComments"]),
    async submitComment() {
      if (this.valid) {
        await axios.post(
          process.env.VUE_APP_API_ENDPOINT + "/comments/create",
          {
            title: this.commentTitle,
            text: this.commentText,
          }
        );
        this.$refs.form.reset();
        this.setComments();
      } else {
        this.$refs.form.validate();
      }
    },
  },
};
</script>

<style>
</style>