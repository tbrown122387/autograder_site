<template>
  <v-container>
    <v-card elevation="2">
      <v-card-title>Card Title</v-card-title>
      <v-card-text>{{ text }}</v-card-text>
      <v-card-actions>
        <v-btn text color="teal" @click="sendRequest">Submit Request</v-btn>
        <v-btn text color="teal" @click="resetText">Reset Request</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => {
    return {
      text: "Send a request to change this text",
    };
  },
  methods: {
    sendRequest() {
      process.env.VUE_APP_API_ENDPOINT;
      axios
        .get(process.env.VUE_APP_API_ENDPOINT + "/api/sample")
        .then((response) => (this.text = response.data));
    },
    resetText() {
      this.text = "Send a request to change this text";
    },
  },
};
</script>

