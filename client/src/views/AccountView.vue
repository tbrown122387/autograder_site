<template>
  <div>
    <div class="mx-auto mt-5 border-2 rounded shadow-lg sm:w-6/12 xl:max-w-2xl">
      <Disclosure v-slot="{ open }">
        <DisclosureButton
          class="w-full px-4 py-2 text-left hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-green-700"
          :class="open ? 'border-b-2 border-gray-400 rounded-t' : '  rounded '"
        >
          <div class="flex items-center justify-between">
            <span>Reset Password</span>
            <i class="fas" :class="open ? 'fa-chevron-up' : 'fa-chevron-down'" />
          </div>
        </DisclosureButton>
        <DisclosurePanel class="px-4">
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
        </DisclosurePanel>
      </Disclosure>
    </div>
    <div class="p-2 mx-auto mt-5 rounded shadow-lg sm:w-6/12 xl:max-w-2xl">
      <TransitionRoot appear :show="isOpen" as="template">
        <Dialog as="div" @close="isOpen = false">
          <div class="fixed inset-0 z-10 overflow-y-auto">
            <div class="min-h-screen px-4 text-center">
              <DialogOverlay class="fixed inset-0 bg-black opacity-60" />

              <span class="inline-block h-screen align-middle" aria-hidden="true"> &#8203; </span>

              <TransitionChild
                as="template"
                enter="duration-300 ease-out"
                enter-from="opacity-0 scale-95"
                enter-to="opacity-100 scale-100"
                leave="duration-200 ease-in"
                leave-from="opacity-100 scale-100"
                leave-to="opacity-0 scale-95"
              >
                <div
                  class="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white border-2 rounded shadow-xl"
                >
                  <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900"> Delete your Account? </DialogTitle>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      This action is irreversible. This will delete all your account information including all assignments.
                    </p>
                  </div>

                  <div class="mt-4">
                    <button type="button" class="p-2 text-white rounded shadow focus:outline-none red-button" @click="closeModal">
                      Confirm Delete
                    </button>
                  </div>
                </div>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>
      <div class="flex flex-col gap-2">
        {{ editText }}
      </div>
      <div class="flex gap-2">
        <button class="flex-1 flex-grow p-2 font-bold text-white rounded shadow focus:outline-none red-button" @click="submitLogOut">
          Log Out
        </button>
        <button class="flex-1 flex-grow p-2 font-bold text-white rounded shadow focus:outline-none red-button" @click="openModal">
          Delete Account
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import {
  Dialog,
  DialogOverlay,
  DialogTitle,
  TransitionRoot,
  TransitionChild,
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/vue";
import { api } from "@/api";
import useVuelidate from "@vuelidate/core";
import { required, minLength, sameAs } from "@vuelidate/validators";
import { getErrorMessage } from "../utils";

export default {
  setup() {
    return { v$: useVuelidate() };
  },
  name: "AccountView",
  components: {
    Dialog,
    DialogOverlay,
    DialogTitle,
    TransitionRoot,
    TransitionChild,
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
  },
  data: function () {
    return {
      isOpen: false,
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
    ...mapActions("AuthModule", ["actionLogOut", "actionCheckLoggedIn"]),
    ...mapActions("RGradingGradescope", ["getAssignments"]),
    submitLogOut() {
      this.actionLogOut().then(() => {
        this.$router.push({ name: "Login" });
      });
    },
    closeModal() {
      api
        .deleteAccount(this.token)
        .then(() => this.actionLogOut().then(() => this.$router.push({ name: "Login" })))
        .catch((error) => console.log(error));
      this.isOpen = false;
    },
    openModal() {
      this.isOpen = true;
    },
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
          .resetPasswordLoggedIn(this.token, this.password)
          .then(() => {
            this.confirmationMessage = "Success";
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
  computed: {
    ...mapState("AuthModule", ["email", "isLoggedIn", "token"]),
    ...mapState("RGradingGradescope", ["listOfAssignments"]),
    editText() {
      if (!this.listOfAssignments.length) {
        return "You have no assignments";
      } else {
        return `${this.listOfAssignments.length} assignments`;
      }
    },
  },
  validations() {
    return {
      password: { required, minLength: minLength(6) },
      confirmPassword: { required, sameAsConfirmPassword: sameAs(this.password) },
    };
  },
  created() {
    this.getAssignments();
  },
};
</script>
