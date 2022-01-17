<template>
  <div>
    <div class="mx-auto mt-5 rounded shadow-lg sm:w-6/12 xl:max-w-2xl">
      <div class="p-6 mb-4 text-3xl text-white bg-green-700 border-b-2 rounded shadow">Request Password Reset</div>
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
          <div v-else>Submit</div>
        </button>
        <div>
          <p>
            {{ confirmationMessage }}
          </p>
        </div>
        <div>
          <router-link :to="{ name: 'Login' }" class="text-green-800 hover:underline focus:outline-none focus:underline">
            Have an Account?
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
import { api } from "@/api";
import { required, email } from "@vuelidate/validators";
import { getErrorMessage } from "../utils";

export default {
  setup() {
    return { v$: useVuelidate() };
  },
  name: "RequestPasswordReset",
  data: function () {
    return {
      inputEmail: "",
      debugData: [],
      vuelidateExternalResults: {
        inputEmail: [],
      },
      loading: false,
      confirmationMessage: "",
    };
  },
  computed: {
    ...mapState("AuthModule", ["isLoggedIn", "isErrorLoggingIn", "errorLoggingIn"]),
  },
  methods: {
    ...mapActions("AuthModule", ["actionGetToken", "actionRegister"]),
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
    async submitForm() {
      const isFormCorrect = await this.v$.$validate();
      if (isFormCorrect && !this.loading) {
        this.loading = true;
        api
          .requestPasswordReset(this.inputEmail)
          .then(() => {
            this.confirmationMessage = "Check your email for instructions on how to reset your password.";
          })
          .catch((error) => {
            if (error.response.status === 400) {
              this.confirmationMessage = "No account exists with that email.";
            } else {
              this.confirmationMessage = "An error occured, please try again later.";
            }
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
  },

  validations() {
    return {
      inputEmail: { required, email },
    };
  },
};
</script>
