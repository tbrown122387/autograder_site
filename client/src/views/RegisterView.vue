<template>
  <v-container>
    <v-row justify="center">
      <v-col xs="12" sm="8" md="6">
        <v-card elevation="2">
          <v-card-title>Create an Account</v-card-title>
          <v-card-text>
            <v-form
              v-model="valid"
              @submit.prevent="submitForm"
              id="registerForm"
              ref="form"
            >
              <v-text-field
                v-model="email"
                prepend-icon="mdi-account"
                name="email"
                label="Email"
                type="text"
                color="teal"
              ></v-text-field>
              <v-text-field
                v-model="password"
                prepend-icon="mdi-lock"
                name="password"
                label="Password"
                id="password"
                color="teal"
                type="password"
              ></v-text-field>
            </v-form>
            <div v-if="isErrorRegistering">
              <v-alert
                :value="isErrorRegistering"
                transition="fade-transition"
                type="error"
              >
                Email already in use.
              </v-alert>
            </div>

            <router-link to="/login"> Back to Login </router-link>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn type="submit" form="registerForm" color="teal" dark>
              Register
            </v-btn>
          </v-card-actions>
          {{ email }}
          {{ password }}
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  name: "RegisterView",
  components: {},
  data: function () {
    return {
      valid: true,
      email: "",
      password: "",
    };
  },
  methods: {
    ...mapActions("Auth", ["actionRegister"]),
    submitForm() {
      this.actionRegister(this.email, this.password).then(() => {
        if (!this.isErrorRegistering) {
          this.$router.push({ path: "login" });
        }
      });
    },
  },
  computed: {
    ...mapState("Auth", ["isLoggedIn", "isErrorRegistering"]),
  },
};
</script>
