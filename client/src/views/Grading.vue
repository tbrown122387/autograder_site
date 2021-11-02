<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header class="text-h6 font-weight-bold">
              Instructions
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              This page is for Autograding with
              <v-chip class="ma-2" label>
                <a href="https://www.gradescope.com/">Gradescope</a>
              </v-chip>
              for R with gradeR.
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
      <v-col cols="12">
        <v-card elevation="3">
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-card flat color="teal lighten-5">
                  <v-card-text>
                    <v-row no-gutters>
                      <v-col cols="12">
                        <v-text-field
                          outlined
                          dense
                          color="teal"
                          value="Untitled01"
                          label="Bundle Name"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12"> Last saved 15 minutes ago </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="12">
                <v-form
                  v-model="valid"
                  @submit.prevent="submitForm"
                  id="gradingForm"
                  ref="form"
                >
                  <v-card elevation="2">
                    <v-card-text>
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="assignmentName"
                            :rules="assignmentNameRules"
                            label="Assignment Name"
                            placeholder="Ex: assignment01.R"
                            required
                          ></v-text-field>
                        </v-col>

                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="packageNames"
                            label="Additional Packages (optional)"
                            placeholder="Ex: survival, data.table, caret"
                          ></v-text-field>
                        </v-col>

                        <v-col cols="12" md="4">
                          <v-file-input
                            label="Datasets (optional)"
                            v-model="datasets"
                            multiple
                          ></v-file-input>
                        </v-col>
                      </v-row>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-progress-linear
                      v-show="loading"
                      indeterminate
                      color="teal"
                    />
                    <v-card-text>
                      <v-row class="mb-2">
                        <v-col cols="6" class="text-right">
                          <v-btn
                            @click="incrementNumberOfTests"
                            color="indigo"
                            dark
                          >
                            Add a Test
                          </v-btn>
                        </v-col>
                        <v-col cols="6">
                          <v-btn
                            @click="decrementNumberOfTests"
                            :disabled="numberOfTests === 1"
                            :dark="numberOfTests !== 1"
                            color="red"
                          >
                            Remove a Test
                          </v-btn>
                        </v-col>
                      </v-row>
                      <v-row v-for="n in numberOfTests" :key="n" no-gutters>
                        <v-col cols="12" md="3" class="px-3">
                          <v-text-field
                            label="Question Label"
                            v-model="labels[n - 1]"
                            :rules="existsRule"
                            color="teal"
                            required
                            outlined
                            dense
                          />
                        </v-col>
                        <v-col cols="12" md="3" class="px-3">
                          <v-select
                            :items="visiblilitySelector"
                            label="Visibility"
                            v-model="visibilities[n - 1]"
                            :rules="existsRule"
                            required
                            outlined
                            dense
                          />
                        </v-col>
                        <v-col cols="12" md="6" class="px-3">
                          <v-text-field
                            label="Code"
                            v-model="codes[n - 1]"
                            :rules="existsRule"
                            required
                            outlined
                            dense
                          />
                          <!-- <MonacoEditor
                            class="editor"
                            v-model="codes[n - 1]"
                            language="python"
                            value="123"
                          /> -->
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-form>
              </v-col>
              <v-col>
                <v-btn
                  elevation="2"
                  type="submit"
                  form="gradingForm"
                  :loading="loading"
                  :disabled="loading"
                  block
                  color="teal"
                  dark
                >
                  Download Bundle
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <!-- <v-row>
      <v-col>
        <v-card elevation="2">
          <v-card-text>{{ numberOfTests }}</v-card-text>
          <v-card-text>{{ packageNames.split(",") }}</v-card-text>
          <v-card-text>{{ datasets.map((file) => file.name) }}</v-card-text>
          <v-card-text>{{ labels }}</v-card-text>
          <v-card-text>{{ visibilities }}</v-card-text>
          <v-card-text>{{ codes }}</v-card-text>
        </v-card>
      </v-col>
    </v-row> -->
  </v-container>
</template>

<script>
import axios from "axios";
// import MonacoEditor from "vue-monaco";
import { mapActions, mapState } from "vuex";

export default {
  components: {
    // MonacoEditor,
  },
  data: () => {
    return {
      loading: false,
      response: "",
      valid: false,
      visiblilitySelector: ["Visible", "After Due Date", "Hidden"],
      assignmentNameRules: [
        (v) => !!v || "Assignment name is required",
        (v) =>
          v.substring(v.length - 2) === ".R" ||
          "Must have valid file ending (.R or .r)",
      ],
      existsRule: [(v) => !!v || "This field is required"],
    };
  },
  computed: {
    numberOfTestsText() {
      return this.numberOfTests > 1 ? "Tests" : "Test";
    },
    ...mapState("RGradingGradescope", ["numberOfTests"]),
    assignmentName: {
      get() {
        return this.$store.state["RGradingGradescope"].assignmentName;
      },
      set(value) {
        this.$store.dispatch("RGradingGradescope/setAssignmentName", value);
      },
    },
    packageNames: {
      get() {
        return this.$store.state["RGradingGradescope"].packageNames;
      },
      set(value) {
        this.$store.dispatch("RGradingGradescope/setPackageNames", value);
      },
    },
    datasets: {
      get() {
        return this.$store.state["RGradingGradescope"].datasets;
      },
      set(value) {
        this.$store.dispatch("RGradingGradescope/setDatasets", value);
      },
    },
    labels: {
      get() {
        return this.$store.state["RGradingGradescope"].labels;
      },
      set(value) {
        this.$store.dispatch("RGradingGradescope/setLabels", value);
      },
    },
    visibilities: {
      get() {
        return this.$store.state["RGradingGradescope"].visibilities;
      },
      set(value) {
        this.$store.dispatch("RGradingGradescope/setVisibilities", value);
      },
    },
    codes: {
      get() {
        return this.$store.state["RGradingGradescope"].codes;
      },
      set(value) {
        this.$store.dispatch("RGradingGradescope/setCodes", value);
      },
    },
  },
  methods: {
    ...mapActions("RGradingGradescope", [
      "incrementNumberOfTests",
      "decrementNumberOfTests",
    ]),
    submitForm() {
      if (this.valid) {
        this.loading = true;
        let formData = new FormData();
        if (this.datasets) {
          // files
          for (let file of this.datasets) {
            formData.append("datasets", file, file.name);
          }
        }

        // additional data
        formData.append("assignment_name", this.assignmentName);
        if (this.packageNames) {
          formData.append(
            "package_names",
            JSON.stringify(this.packageNames.split(","))
          );
        }

        formData.append("labels", JSON.stringify(this.labels));
        formData.append("visibilities", JSON.stringify(this.visibilities));
        formData.append("codes", JSON.stringify(this.codes));
        axios
          .post(process.env.VUE_APP_API_ENDPOINT + "/uploadfile", formData, {
            responseType: "blob",
          })
          .then((response) => {
            console.log("Success!");
            console.log(response);
            const blob = new Blob([response.data], { type: "application/zip" });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "data";
            link.click();
            URL.revokeObjectURL(link.href);
          })
          .catch((error) => {
            console.log({ error });
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        this.$refs.form.validate();
      }
    },
  },
};
</script>

