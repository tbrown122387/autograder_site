<template>
  <div>
    <div class="mx-auto mt-5 rounded shadow-lg sm:w-6/12 xl:max-w-2xl">
      <div class="p-6 mb-4 text-3xl text-white bg-green-700 border-b-2 rounded shadow">Create an Account</div>
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
          class="w-full p-2 font-bold text-white transition duration-100 rounded shadow focus:outline-none"
          :class="loading ? 'bg-gray-700 cursor-default' : 'green-button'"
          :disabled="loading"
          @click="submitForm"
        >
          <div v-if="loading">
            <i class="fas fa-circle-notch animate-spin" />
            Processing
          </div>
          <div v-else>Register</div>
        </button>

        <div>
          <router-link :to="{ name: 'Login' }" class="text-green-800 hover:underline focus:outline-none focus:underline">
            Have an Account?
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
  name: "RegisterView",
  components: {},
  data: function () {
    return {
      inputEmail: "",
      password: "",
      debugData: [],
      vuelidateExternalResults: { inputEmail: [], password: [] },
      loading: false,
    };
  },
  computed: {
    ...mapState("AuthModule", ["isLoggedIn", "isErrorRegistering", "errorRegistering"]),
  },
  methods: {
    ...mapActions("AuthModule", ["actionGetToken", "actionRegister"]),
    getErrorText(error, fieldData) {
      return getErrorMessage(error, fieldData);
    },

    changeEmail(e) {
      this.inputEmail = e.target.value;
      this.v$.inputEmail.$touch();
      if (this.isErrorRegistering) {
        this.v$.$clearExternalResults();
      }
    },
    changePassword(e) {
      this.password = e.target.value;
      this.v$.password.$touch();
      if (this.isErrorRegistering) {
        this.v$.$clearExternalResults();
      }
    },
    async submitForm() {
      const isFormCorrect = await this.v$.$validate();
      if (isFormCorrect && !this.loading) {
        this.loading = true;
        this.actionRegister(this.inputEmail, this.password)
          .then(() => {
            if (this.isErrorRegistering && this.errorRegistering.error.response.status == 400) {
              const errors = {
                inputEmail: ["Email already exists."],
              };
              Object.assign(this.vuelidateExternalResults, errors);
            }
            if (!this.isErrorRegistering) {
              this.$router.push({ path: "login" });
            }
          })
          .catch(() => {
            const errors = {
              inputEmail: ["Email already exists."],
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
