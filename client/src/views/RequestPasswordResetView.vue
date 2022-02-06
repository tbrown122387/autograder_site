<template>
  <div>
    <div class="mx-auto mt-5 rounded shadow-lg sm:w-6/12 xl:max-w-2xl">
      <div class="p-6 mb-4 text-3xl text-white bg-green-700 border-b-2 rounded shadow">Request Password Reset</div>
      <div class="flex flex-col gap-2 p-4">
        <input
          class="textbox"
          :class="v$.email.$error && 'error'"
          type="text"
          placeholder="Email"
          :value="email"
          @input="changeEmail"
          @keyup.enter="submitForm"
        />
        <div class="text-xs text-red-500" :class="v$.email.$error ? 'visible' : 'invisible'">
          {{ getErrorText(v$.email.$errors, { name: "Email" }) }}
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
      email: "",
      debugData: [],
      vuelidateExternalResults: {
        email: [],
      },
      loading: false,
      confirmationMessage: "",
    };
  },
  methods: {
    getErrorText(error, fieldData) {
      return getErrorMessage(error, fieldData);
    },

    changeEmail(e) {
      this.email = e.target.value;
      this.v$.email.$touch();
      this.v$.$clearExternalResults();
    },
    async submitForm() {
      const isFormCorrect = await this.v$.$validate();
      if (isFormCorrect && !this.loading) {
        this.loading = true;
        api
          .requestPasswordReset(this.email)
          .then(() => {
            this.confirmationMessage = "Check your email for instructions on how to reset your password.";
          })
          .catch((error) => {
            if (error.response.status == 400) {
              const errors = {
                email: ["No account exists with that email."],
              };
              Object.assign(this.vuelidateExternalResults, errors);
            } else {
              const errors = {
                email: ["An error occured, please try again later."],
              };
              Object.assign(this.vuelidateExternalResults, errors);
            }
            this.confirmationMessage = "";
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
  },

  validations() {
    return {
      email: { required, email },
    };
  },
};
</script>
