<template>
  <div class="p-6 mx-auto mt-5 border-2 shadow-lg md:w-9/12 xl:max-w-4xl">
    <div class="flex flex-col gap-2">
      <button
        class="w-full p-2 font-bold text-white transition duration-100 rounded shadow focus:outline-none"
        :class="isCreatingAssignment ? 'bg-gray-700 cursor-default' : 'green-button'"
        :disabled="isCreatingAssignment"
        @click="clickCreateAssignment"
      >
        <div v-if="isCreatingAssignment">
          <i class="fas fa-circle-notch animate-spin" />
          Creating Assignment
        </div>
        <div v-else>Create Assignment</div>
      </button>

      <div v-if="listOfAssignments.length" class="flex items-center">
        <input class="checkbox" id="deleteModeCheckbox" type="checkbox" v-model="isDeleteModeOn" />
        <label class="ml-1 mr-2 cursor-pointer" for="deleteModeCheckbox"> Delete Mode </label>
      </div>
      <div
        v-for="assignment in listOfAssignments"
        :key="assignment.id"
        :class="assignment.id === assignmentToEditId ? 'border-l-2 border-green-600' : ''"
      >
        <div
          class="flex items-center flex-grow gap-2 p-2"
          :class="assignment.id === assignmentToEditId ? 'border-t-2 border-b-2 border-r-2 rounded-r' : 'border-2 rounded'"
        >
          <button class="w-8 h-8 blue-button" @click="openTest(assignment.id)">
            <i class="fas fa-external-link-alt" />
          </button>
          <button
            class="w-8 h-8 text-white transition duration-100 ease-linear rounded shadow focus:outline-none"
            @click="removeTest(assignment.id)"
            :class="!isDeleteModeOn ? 'bg-gray-600 cursor-default' : 'red-button'"
            :disabled="!isDeleteModeOn"
          >
            <i class="fas fa-trash-alt" />
          </button>

          <div class="flex flex-grow gap-2">
            <div>
              {{ getBundleNameText(assignment.bundleName) }}
            </div>
            <div class="flex-grow"></div>
            <div>Last modified {{ format(assignment.lastModified) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";
import { formatDistanceToNowStrict } from "date-fns";
export default {
  name: "ListView",
  data: () => {
    return {
      isDeleteModeOn: false,
      isCreatingAssignment: false,
    };
  },
  computed: {
    ...mapState("RGradingGradescope", ["assignmentToEditId", "listOfAssignments"]),
    ...mapState("AuthModule", ["isLoggedIn"]),
  },
  methods: {
    ...mapActions("RGradingGradescope", ["getAssignments", "createAssignment", "deleteAssignment"]),
    ...mapMutations("RGradingGradescope", ["setAssignmentToEditId"]),
    getBundleNameText(bundleName) {
      return bundleName ? bundleName : "Untitled";
    },
    removeTest(assignmentId) {
      this.deleteAssignment(assignmentId);
    },
    openTest(assignmentId) {
      this.setAssignmentToEditId(assignmentId);
      this.$router.push({ name: "Edit" });
    },
    format(date) {
      return formatDistanceToNowStrict(date - 1000, { addSuffix: true }); // subtract 1 second to account for slight server differences
    },
    clickCreateAssignment() {
      this.isCreatingAssignment = true;
      this.createAssignment()
        .catch((error) => console.log({ error }))
        .finally(() => {
          this.isCreatingAssignment = false;
        });
    },
  },
  created() {
    const loadAssignments = () => {
      if (this.isLoggedIn) {
        this.getAssignments();
      } else {
        this.$router.push({ name: "Login" });
      }
    };
    loadAssignments();
    this.timer = setInterval(loadAssignments, 5000);
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
};
</script>
