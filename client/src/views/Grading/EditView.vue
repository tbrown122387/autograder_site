<template>
  <div>
    <div class="mx-auto mt-5 border-2 rounded shadow-lg md:w-11/12 xl:max-w-7xl">
      <Disclosure v-slot="{ open }">
        <DisclosureButton
          class="w-full px-4 py-2 text-left hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-green-700"
          :class="open ? 'border-b-2 border-gray-400 rounded-t' : '  rounded '"
        >
          <div class="flex items-center justify-between">
            <span>Instructions</span>
            <i class="fas" :class="open ? 'fa-chevron-up' : 'fa-chevron-down'" />
          </div>
        </DisclosureButton>
        <DisclosurePanel class="px-4">
          <div class="px-2 pt-2 pb-1 text-gray-500">
            This page is for Autograding with Gradescope for R with gradeR. After filling out the required fields, the website produces a
            <code>data.zip</code>, which can then be uploaded to Gradescope.
          </div>
          <span>Assignment Name</span>
          <div class="px-2 pt-2 pb-1 text-gray-500">
            Assignment name is required. It is the name of the assignment that students submit to Gradescope. Every submission has to have
            this title, or the autograder will not work properly. In addition, the file names are case-sensitive.
          </div>
          <span>Additional Packages</span>
          <div class="px-2 pt-2 pb-1 text-gray-500">
            If there are any additional packages needed, list them here with a comma in between. Currently, there is not support for a
            set-up section for tests (for calling <code>library()</code>), so tests involving libraries need to prefaced for each function,
            e.g. <code>stringr::str_count()</code>. Students can still use libraries as normal.
          </div>
          <span>Datasets</span>
          <div class="px-2 pt-2 pb-1 text-gray-500">
            As many datasets can be added as desired, but the total size must be less than 10 MB (This will change in future updates).
            Students must reference the dataset from the same directory as the submission file, i.e.
            <code>read.csv("dataset.csv")</code>. The following will not work <code>read.csv("data/dataset.csv")</code>. The working
            directory should not be changed either, so students must comment out <code>setwd()</code> if used.
          </div>
          <span>Tests</span>
          <div class="px-2 pt-2 pb-1 text-gray-500">
            At least one test is required to create the bundle. The code section for each test expects a <code>TRUE</code> if the answer is
            correct.
          </div>
        </DisclosurePanel>
      </Disclosure>
    </div>
    <div v-if="isPageLoaded" class="mx-auto mt-5 rounded shadow-lg md:w-11/12 xl:max-w-7xl">
      <div class="flex flex-col bg-gray-100 rounded">
        <div v-if="isLoggedIn" class="flex flex-col gap-4 mx-4 mt-4 mb-5">
          <div class="flex items-center justify-between gap-2">
            <router-link :to="{ name: 'List' }" class="px-2 py-1 font-bold green-button">
              <i class="fas fa-chevron-left" />
              Back to List
            </router-link>
            <div>
              <span v-if="!hasChanged" class="text-green-700">Autosaved <i class="fas fa-check" /></span>
              <span v-else class="text-green-700">Saving <i class="fas fa-circle-notch animate-spin" /></span>

              <!-- <button
                class="px-2 py-1 font-bold rounded shadow"
                :class="hasChanged || isSaving ? 'blue-button' : 'bg-gray-400 cursor-default'"
                :disabled="!hasChanged || isSaving"
                @click="clickSaveButton"
              >
                <span v-if="isSaving"> Autosaving <i class="fas fa-circle-notch animate-spin" /> </span>
                <span v-else-if="hasChanged"> Save </span>
                <span v-else> Saved </span>
              </button> -->
            </div>
          </div>

          <div>
            <input class="textbox" :class="v$.bundleName.$error && 'error'" type="text" placeholder="Bundle Name" v-model="bundleName" />
            <div class="absolute text-xs text-red-500" v-show="v$.bundleName.$error">
              {{ getErrorText(v$.bundleName.$errors, { name: "Bundle Name" }) }}
            </div>
          </div>

          <!-- <p v-for="error of v$.$errors" :key="error.$uid">{{ error }}</p> -->
        </div>
        <div v-else class="mx-4 mt-4 mb-2">
          <div class="p-2 text-orange-700 bg-orange-100 border-l-4 border-orange-500" role="alert">
            <p class="font-bold">
              <i class="fas fa-exclamation-triangle"></i>
              Your Progress Will Not be Saved
            </p>

            <router-link
              :to="{ name: 'Login' }"
              class="p-1 underline transition duration-100 ease-linear rounded hover:shadow hover:no-underline focus:outline-none focus:bg-white hover:bg-white"
              >Login</router-link
            >
            <span> or </span>
            <router-link
              :to="{ name: 'Register' }"
              class="p-1 underline transition duration-100 ease-linear rounded hover:shadow hover:no-underline focus:outline-none focus:bg-white hover:bg-white"
            >
              Create an Account
            </router-link>
          </div>
        </div>

        <div class="flex flex-col gap-2 p-2 mx-4 mb-4 bg-white border-gray-200 rounded shadow-md">
          <div class="grid items-center justify-center grid-cols-6 gap-2 lg:grid-cols-12">
            <div class="col-span-6 my-4">
              <input
                class="textbox"
                :class="v$.assignmentName.$error && 'error'"
                type="text"
                placeholder="Assignment Name"
                v-model="assignmentName"
              />
              <div class="absolute text-xs text-red-500" v-show="v$.assignmentName.$error">
                {{
                  getErrorText(v$.assignmentName.$errors, {
                    name: "Assignment Name",
                  })
                }}
              </div>
            </div>
            <div class="flex flex-wrap justify-center col-span-6">
              <div class="flex items-center">
                <input class="checkbox" id="rmarkdownCheckbox" type="checkbox" v-model="isRMarkdownSelected" />
                <label class="ml-1 mr-2 cursor-pointer" for="rmarkdownCheckbox"> R Markdown </label>
              </div>

              <div class="flex items-center">
                <input class="checkbox" id="datasetCheckbox" type="checkbox" v-model="isDatasetsSelected" />
                <label class="ml-1 mr-2 cursor-pointer" for="datasetCheckbox"> Dataset(s) </label>
              </div>
              <div class="flex items-center">
                <input class="checkbox" id="packageCheckbox" type="checkbox" v-model="isPackagesSelected" />
                <label class="ml-1 mr-2 cursor-pointer" for="packageCheckbox"> Package(s) </label>
              </div>
              <div class="flex items-center">
                <input class="checkbox" id="setupCheckbox" type="checkbox" v-model="isSetupSelected" />
                <label class="ml-1 mr-2 cursor-pointer" for="setupCheckbox"> Setup </label>
              </div>
            </div>
          </div>
          <div class="flex flex-wrap gap-2">
            <div v-if="isPackagesSelected" class="flex-1">
              <input class="textbox" type="text" placeholder="Packages" v-model="packageNames" />
            </div>
            <div v-if="isDatasetsSelected" class="flex-1">
              <label
                class="flex gap-2 transition duration-150 ease-linear bg-white border border-gray-500 rounded shadow-md cursor-pointer hover:border-green-800"
              >
                <div class="px-4 py-2 bg-gray-200 rounded-l">
                  <i class="fas fa-cloud-upload-alt" />
                </div>
                <span v-if="!fileNames.length || !isDatasetsSynced" class="py-2 pr-4">Dataset(s)</span>
                <span v-else class="py-2 pr-4 font-mono"> {{ fileNames.join(", ") }}</span>
                <input type="file" class="hidden" multiple @change="onFileChange" />
              </label>
              <div v-if="!isDatasetsSynced" class="p-2 text-red-700 bg-red-100 border-l-4 border-red-500" role="alert">
                <p class="font-bold">
                  <i class="fas fa-exclamation-circle" />
                  This website does not store your dataset(s), please reupload the following:
                  <span class="font-mono text-sm">{{ fileNames.join(", ") }}</span>
                </p>
              </div>
            </div>
          </div>
          <div v-if="isSetupSelected" class="flex flex-grow">
            <div class="flex flex-col flex-grow">
              <div class="text-sm text-gray-500">Setup Code (initalize libraries and create utility variables)</div>
              <textarea
                v-model="setupCode"
                class="w-full font-mono text-sm rounded focus:border-green-800 focus:ring-green-800"
                :placeholder="setupPlaceholderText"
                rows="10"
              />
            </div>
          </div>
          <div class="grid grid-cols-12">
            <button class="w-full col-span-12 p-2 font-bold blue-button" @click="incrementNumberOfTests">Add Test</button>
          </div>

          <TestCollection
            v-for="(test, index) in testsCollection"
            :key="index"
            :index="index"
            :visibility="test.visibility"
            :label="test.label"
            :code="test.code"
            @update-visibility="(value, index) => updateTestsCollection('visibility', index, value)"
            @update-label="(value, index) => updateTestsCollection('label', index, value)"
            @update-code="(value, index) => updateTestsCollection('code', index, value)"
            @remove-test="(index) => removeTest(index)"
          />
          <div class="grid grid-cols-12">
            <button
              class="w-full col-span-12 p-2 font-bold text-white transition duration-100 rounded shadow focus:outline-none"
              :class="loading ? 'bg-gray-700 cursor-default' : 'green-button'"
              :disabled="loading"
              @click="submitForm"
            >
              <div v-if="loading">
                <i class="fas fa-circle-notch animate-spin" />
                Processing
              </div>
              <div v-else>Download Bundle</div>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="mx-auto mt-5 rounded shadow-lg md:w-11/12 xl:max-w-7xl">
      <div class="flex flex-col bg-gray-100 rounded">
        <div class="mx-auto mt-4 mb-5">
          <span><i class="text-gray-300 fas fa-10x fa-circle-notch animate-spin" /></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import TestCollection from "@/components/TestCollection.vue";
import { api } from "@/api";
import { autoDownloadFile, getErrorMessage } from "@/utils";
import { mapActions, mapMutations, mapState, mapGetters } from "vuex";
import useVuelidate from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";

const properFileType = (value) => value.substring(value.length - 4) === ".Rmd" || value.substring(value.length - 2).toLowerCase() === ".r";

export default {
  name: "EditView",
  setup() {
    return { v$: useVuelidate() };
  },
  created() {
    if (this.isLoggedIn) {
      if (this.listOfAssignments.map((assignment) => assignment.id).includes(this.assignmentToEditId)) {
        this.getAssignment().then(() => (this.isPageLoaded = true));
        const saveAssignment = () => {
          if (this.isLoggedIn) {
            this.clickSaveButton();
          }
        };
        this.timer = setInterval(saveAssignment, 5000);
      } else {
        this.$router.push({ name: "List" });
      }
    } else {
      this.isPageLoaded = true;
    }
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
  components: {
    Disclosure,
    DisclosureButton,
    DisclosurePanel,
    TestCollection,
  },
  data: () => {
    return {
      setupPlaceholderText: "Ex:\nlibrary(stringr)\n\nq1.ans <- c(4,5,6)",
      codePlaceholderText: "Ex:length(lm.mod$coefficients) == 4",
      loading: false,
      hasChanged: false,
      isPageLoaded: true,
    };
  },
  computed: {
    ...mapState("RGradingGradescope", ["datasets", "fileNames", "listOfAssignments", "assignmentToEditId", "lastModified"]),
    ...mapState("AuthModule", ["isLoggedIn", "email"]),
    ...mapGetters("RGradingGradescope", ["numberOfTests", "isDatasetsSynced"]),
    isRMarkdownSelected: {
      get() {
        return this.$store.state["RGradingGradescope"].isRMarkdownSelected;
      },
      set(value) {
        return this.$store.commit("RGradingGradescope/setIsRMarkdownSelected", value);
      },
    },
    isDatasetsSelected: {
      get() {
        return this.$store.state["RGradingGradescope"].isDatasetsSelected;
      },
      set(value) {
        return this.$store.commit("RGradingGradescope/setIsDatasetsSelected", value);
      },
    },
    isPackagesSelected: {
      get() {
        return this.$store.state["RGradingGradescope"].isPackagesSelected;
      },
      set(value) {
        return this.$store.commit("RGradingGradescope/setIsPackagesSelected", value);
      },
    },
    isSetupSelected: {
      get() {
        return this.$store.state["RGradingGradescope"].isSetupSelected;
      },
      set(value) {
        return this.$store.commit("RGradingGradescope/setIsSetupSelected", value);
      },
    },
    setupCode: {
      get() {
        return this.$store.state["RGradingGradescope"].setupCode;
      },
      set(value) {
        this.hasChanged = true;
        return this.$store.commit("RGradingGradescope/setSetupCode", value);
      },
    },
    bundleName: {
      get() {
        return this.$store.state["RGradingGradescope"].bundleName;
      },
      set(value) {
        this.hasChanged = true;
        this.$store.commit("RGradingGradescope/setBundleName", value);
        this.v$.bundleName.$touch();
      },
    },
    assignmentName: {
      get() {
        return this.$store.state["RGradingGradescope"].assignmentName;
      },
      set(value) {
        this.hasChanged = true;
        this.$store.commit("RGradingGradescope/setAssignmentName", value);
        this.v$.assignmentName.$touch();
      },
    },
    packageNames: {
      get() {
        return this.$store.state["RGradingGradescope"].packageNames;
      },
      set(value) {
        this.hasChanged = true;
        this.$store.commit("RGradingGradescope/setPackageNames", value);
      },
    },
    testsCollection: {
      get() {
        return this.$store.state["RGradingGradescope"].testsCollection;
      },
      // set(value) {
      //   this.$store.commit("RGradingGradescope/setTestsCollection", value);
      // },
    },
  },
  methods: {
    ...mapActions("RGradingGradescope", [
      "incrementNumberOfTests",
      "removeTest",
      "saveAssignment",
      "getAssignment",
      "clearAssignmentStore",
    ]),
    ...mapMutations("RGradingGradescope", ["setDatasets", "setTestsCollection"]),
    getVisibilityText(text) {
      return this.visiblilitySelector.filter((obj) => obj.value === text)[0].text;
    },
    onFileChange(e) {
      this.hasChanged = true;
      var files = e.target.files || e.dataTransfer.files;
      if (files.length) {
        this.setDatasets(files);
      }
    },
    getErrorText(error, fieldData) {
      return getErrorMessage(error, fieldData);
    },
    clickSaveButton() {
      if (this.hasChanged) {
        this.saveAssignment()
          .catch((error) => console.log({ error }))
          .finally(() => {
            this.hasChanged = false;
          });
      }
    },
    updateTestsCollection(type, index, value) {
      this.hasChanged = true;
      const newTestsCollection = this.testsCollection.map((test, iterIndex) => {
        if (iterIndex === index) {
          return { ...test, [type]: value }; // "[]" evaluates variable
        } else {
          return { ...test };
        }
      });
      this.setTestsCollection(newTestsCollection);
    },
    async submitForm() {
      this.v$.$reset();
      const isFormCorrect = await this.v$.$validate();
      if (isFormCorrect) {
        this.loading = true;
        api
          .downloadBundle(this.assignmentName, this.datasets, this.packageNames, this.testsCollection)
          .then((response) => {
            autoDownloadFile(response);
          })
          .catch((error) => console.log({ error }))
          .finally(() => (this.loading = false));
      }
    },
  },
  validations() {
    return {
      bundleName: { required },
      assignmentName: {
        required,
        properFileType: helpers.withMessage("Must have valid file ending (.R, .r, or .Rmd)", properFileType),
      },
    };
  },
};
</script>
