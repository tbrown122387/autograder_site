<template>
  <div>
    <div class="mx-auto mt-5 rounded shadow-lg sm:w-6/12 xl:max-w-2xl">
      <div class="p-6 mb-4 text-3xl text-white bg-green-700 border-b-2 rounded shadow">Login</div>
      <div class="flex flex-col gap-2 p-4">
        <input
          class="textbox"
          :class="v$.inputEmail.$error && 'error'"
          type="text"
          placeholder="Email"
          :value="inputEmail"
          @input="changeEmail"
          @keyup.enter="submitForm"
        />
        <div class="text-xs text-red-500" :class="v$.inputEmail.$error ? 'visible' : 'invisible'">
          {{ getErrorText(v$.inputEmail.$errors, { name: "Email" }) }}
        </div>
        <input
          class="textbox"
          :class="v$.password.$error && 'error'"
          type="password"
          placeholder="Password"
          :value="password"
          @input="changePassword"
          @keyup.enter="submitForm"
        />
        <div class="text-xs text-red-500" :class="v$.password.$error ? 'visible' : 'invisible'">
          {{ getErrorText(v$.password.$errors, { name: "Password", length: 6 }) }}
        </div>
        <button
          class="w-full p-2 font-bold text-white rounded shadow focus:outline-none"
          :class="loading ? 'bg-gray-700 cursor-default' : 'green-button'"
          :disabled="loading"
          @click="submitForm"
        >
          <div v-if="loading">
            <i class="fas fa-circle-notch animate-spin" />
            Processing
          </div>
          <div v-else>Login</div>
        </button>

        <div>
          <router-link :to="{ name: 'RequestPasswordReset' }" class="text-green-800 hover:underline focus:outline-none focus:underline">
            Forgot your Password?
          </router-link>
        </div>
        <div>
          <router-link :to="{ name: 'Register' }" class="text-green-800 hover:underline focus:outline-none focus:underline">
            Create an Account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import useVuelidate from "@vuelidate/core";
import { required, email, minLength } from "@vuelidate/validators";
import { getErrorMessage } from "../utils";

export default {
  setup() {
    return { v$: useVuelidate() };
  },
  name: "LoginView",
  data: function () {
    return {
      inputEmail: "",
      password: "",
      debugData: [],
      vuelidateExternalResults: {
        inputEmail: [],
        password: [],
      },
      loading: false,
    };
  },
  computed: {
    ...mapState("AuthModule", ["isLoggedIn", "isErrorLoggingIn", "errorLoggingIn"]),
  },
  methods: {
    ...mapActions("AuthModule", ["actionGetToken"]),
    getErrorText(error, fieldData) {
      return getErrorMessage(error, fieldData);
    },

    changeEmail(e) {
      this.inputEmail = e.target.value;
      this.v$.inputEmail.$touch();
      if (this.isErrorLoggingIn) {
        this.v$.$clearExternalResults();
      }
    },
    changePassword(e) {
      this.password = e.target.value;
      this.v$.password.$touch();
      if (this.isErrorLoggingIn) {
        this.v$.$clearExternalResults();
      }
    },
    async submitForm() {
      const isFormCorrect = await this.v$.$validate();
      if (isFormCorrect && !this.loading) {
        this.loading = true;
        this.actionGetToken({ email: this.inputEmail, password: this.password })
          .then(() => {
            if (this.isErrorLoggingIn && this.errorLoggingIn.error.response.status == 401) {
              const errors = {
                inputEmail: ["\xa0"],
                password: ["Incorrect email or password."],
              };
              Object.assign(this.vuelidateExternalResults, errors);
            } else if (!this.isErrorLoggingIn) {
              this.$router.push({ name: "Account" });
            }
          })
          .catch(() => {
            const errors = {
              inputEmail: ["\xa0"],
              password: ["An error occured, please try again later."],
            };
            Object.assign(this.vuelidateExternalResults, errors);
          })
          .finally(() => (this.loading = false));
      }
    },
  },

  validations() {
    return {
      inputEmail: { required, email },
      password: { required, minLength: minLength(6) },
    };
  },
};
</script>
