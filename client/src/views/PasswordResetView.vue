<template>
  <div>
    <div class="mx-auto mt-5 rounded shadow-lg sm:w-6/12 xl:max-w-2xl">
      <div class="p-6 mb-4 text-3xl text-white bg-green-700 border-b-2 rounded shadow">Reset Password</div>
      <div class="flex flex-col gap-2 p-4">
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
        <input
          class="textbox"
          :class="v$.confirmPassword.$error && 'error'"
          type="password"
          placeholder="Confirm Password"
          :value="confirmPassword"
          @input="changeConfirmPassword"
          @keyup.enter="submitForm"
        />
        <div class="text-xs text-red-500" :class="v$.confirmPassword.$error ? 'visible' : 'invisible'">
          {{ getErrorText(v$.confirmPassword.$errors, { name: "Confirm Password" }) }}
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
          <div v-else>Reset Password</div>
        </button>
        <div>
          <p>
            {{ confirmationMessage }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import useVuelidate from "@vuelidate/core";
import { api } from "@/api";
import { required, minLength, sameAs } from "@vuelidate/validators";
import { getErrorMessage } from "../utils";

export default {
  setup() {
    return { v$: useVuelidate() };
  },
  name: "PasswordReset",
  components: {},
  data: function () {
    return {
      password: "",
      confirmPassword: "",
      confirmationMessage: "",
      loading: false,
      vuelidateExternalResults: {
        password: [],
      },
    };
  },
  methods: {
    getErrorText(error, fieldData) {
      return getErrorMessage(error, fieldData);
    },
    changePassword(e) {
      this.password = e.target.value;
      this.v$.password.$touch();
    },
    changeConfirmPassword(e) {
      this.confirmPassword = e.target.value;
      this.v$.confirmPassword.$touch();
    },
    async submitForm() {
      const isFormCorrect = await this.v$.$validate();
      if (isFormCorrect && !this.loading) {
        this.loading = true;
        api
          .resetPasswordToken(this.$route.query.email, this.password, this.$route.query.token)
          .then(() => {
            this.confirmationMessage = "Success, please close this page";
          })
          .catch(() => {
            const errors = {
              password: ["An error occured, please try again later"],
            };
            Object.assign(this.vuelidateExternalResults, errors);
          })
          .finally(() => (this.loading = false));
      }
    },
  },
  validations() {
    return {
      password: { required, minLength: minLength(6) },
      confirmPassword: { required, sameAsConfirmPassword: sameAs(this.password) },
    };
  },
};
</script>
