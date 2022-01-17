<template>
  <div class="flex items-center gap-2 mb-4">
    <button
      class="w-8 h-8 text-white rounded shadow focus:outline-none"
      :class="numberOfTests <= 1 ? 'bg-gray-600 cursor-default' : 'red-button'"
      :disabled="numberOfTests <= 1"
      @click="$emit('removeTest', index)"
    >
      <i class="fas fa-trash-alt" />
    </button>
    <div class="grid items-center w-full grid-cols-12 gap-2">
      <div class="col-span-3">
        <Listbox v-model="visibilityModel">
          <div class="relative">
            <ListboxButton
              class="relative w-full px-4 py-2 text-left text-gray-500 transition duration-200 border rounded cursor-pointer focus:outline-none"
              :class="
                v$.visibilityModel.$error
                  ? 'border-red-500 focus:border-red-500  focus:ring-1 focus:ring-red-500 '
                  : 'border-gray-500 focus:border-green-800 focus:ring-1 focus:ring-green-800'
              "
            >
              <span class="block mr-5 truncate">
                {{ getVisibilityText(visibility) }}
              </span>
              <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                <i class="text-gray-500 fas fa-chevron-down" />
              </span>
            </ListboxButton>

            <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
              <ListboxOptions
                class="absolute z-50 w-40 py-1 mt-1 overflow-auto text-base bg-white rounded-md shadow-lg max-h-60 ring-2 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
              >
                <ListboxOption
                  v-slot="{ active, selected }"
                  v-for="option in visiblilitySelector"
                  :key="option.value"
                  :value="option.value"
                  as="template"
                >
                  <li
                    :class="[
                      active ? 'text-green-900 bg-green-100' : 'text-gray-900',
                      'cursor-pointer select-none relative py-2 pl-10 pr-4',
                    ]"
                  >
                    <span :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">{{ option.text }} </span>
                    <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-green-600">
                      <i class="fas fa-check" />
                    </span>
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </transition>
          </div>
        </Listbox>

        <div class="absolute text-xs text-red-500" v-show="v$.visibilityModel.$error">
          {{ getErrorText(v$.visibilityModel.$errors, { name: "Visibility" }) }}
        </div>
      </div>
      <div class="col-span-3">
        <input type="text" v-model="labelModel" class="textbox" :class="v$.labelModel.$error && 'error'" placeholder="Label" />

        <div class="absolute text-xs text-red-500" v-show="v$.labelModel.$error">
          {{ getErrorText(v$.labelModel.$errors, { name: "Label" }) }}
        </div>
      </div>
      <div class="col-span-6">
        <div class="flex">
          <textarea
            v-model="codeModel"
            class="w-full font-mono transition duration-200 rounded"
            :class="
              v$.codeModel.$error
                ? 'text-red-500 focus:border-red-500 border-red-500 focus:ring-red-500'
                : 'focus:border-green-800 focus:ring-green-800'
            "
            placeholder="Code"
            rows="1"
          />
        </div>

        <div class="absolute text-xs text-red-500" v-show="v$.codeModel.$error">
          {{ getErrorText(v$.codeModel.$errors, { name: "Code" }) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import useVuelidate from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { mapGetters } from "vuex";
import { getErrorMessage } from "../utils";
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from "@headlessui/vue";

export default {
  setup() {
    return {
      v$: useVuelidate(),
    };
  },
  components: {
    Listbox,
    ListboxButton,
    ListboxOptions,
    ListboxOption,
  },
  props: {
    index: Number,
    visibility: String,
    label: String,
    code: String,
  },
  emits: ["removeTest", "updateVisibility", "updateLabel", "updateCode"],
  data() {
    return {
      visiblilitySelector: [
        { text: "Select Visibility", value: "" },
        { text: "Visible", value: "visible" },
        { text: "After Due Date", value: "after_due_date" },
        { text: "After Published", value: "after_published" },
        { text: "Hidden", value: "hidden" },
      ],
    };
  },
  computed: {
    ...mapGetters("RGradingGradescope", ["numberOfTests"]),
    visibilityModel: {
      get() {
        return this.visibility;
      },
      set(value) {
        this.v$.visibilityModel.$touch();
        this.$emit("updateVisibility", value, this.index);
      },
    },
    labelModel: {
      get() {
        return this.label;
      },
      set(value) {
        this.v$.labelModel.$touch();
        this.$emit("updateLabel", value, this.index);
      },
    },
    codeModel: {
      get() {
        return this.code;
      },
      set(value) {
        this.v$.codeModel.$touch();
        this.$emit("updateCode", value, this.index);
      },
    },
  },
  methods: {
    getVisibilityText(text) {
      return this.visiblilitySelector.filter((obj) => obj.value === text)[0].text;
    },
    getErrorText(error, fieldData) {
      return getErrorMessage(error, fieldData);
    },
  },
  validations() {
    return {
      visibilityModel: { required },
      labelModel: { required },
      codeModel: { required },
    };
  },
};
</script>
