<template>
  <v-container>
    <v-row justify="center">
      <v-col xs="12" sm="8" md="6">
        <v-card elevation="2">
          <v-card-title> Email: {{ email }} </v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  name: "AccountView",
  components: {},
  data: function () {
    return {};
  },
  methods: {
    ...mapActions("Auth", [""]),
  },
  computed: {
    ...mapState("Auth", ["email"]),
  },
};
</script>
