import { compareDesc } from "date-fns";
import { api } from "@/api";

const state = () => ({
  bundleName: "",
  assignmentName: "",
  packageNames: "",
  isDatasetsSelected: false,
  isPackagesSelected: false,
  isSetupSelected: false,
  setupCode: "",
  datasets: [],
  fileNames: [],
  testsCollection: [{ label: "", visibility: "", code: "" }],
  assignmentToEditId: null,
  listOfAssignments: [],
  lastModified: null,
});

const getters = {
  fileNames: (state) => {
    return state.fileNames;
  },
  numberOfTests: (state) => state.testsCollection.length,
  isDatasetsSynced: (state) => {
    const datasets = [...state.datasets].map((file) => file.name).sort();
    const fileNames = [...state.fileNames].sort();
    return datasets.length === fileNames.length && datasets.every((val, index) => val === fileNames[index]);
  },
};

const actions = {
  incrementNumberOfTests: function ({ commit, state }) {
    commit("setTestsCollection", [...state.testsCollection, { label: "", visibility: "", code: "" }]);
  },
  removeTest: function ({ commit, state, getters }, testIndex) {
    if (getters.numberOfTests > 1) {
      commit(
        "setTestsCollection",
        state.testsCollection.filter((value, index) => index !== testIndex)
      );
    }
  },
  getAssignments: function ({ commit, rootState, dispatch }) {
    api
      .getAssignments(rootState.AuthModule.token)
      .then((response) => {
        const listOfAssignments = response.data.map((assignment) => {
          return {
            id: assignment.id,
            bundleName: assignment.bundle_name,
            lastModified: Date.parse(assignment.last_modified),
          };
        });

        listOfAssignments.sort((a, b) => compareDesc(a.lastModified, b.lastModified));
        commit("setListOfAssignments", listOfAssignments);
      })
      .catch((error) => {
        dispatch("AuthModule/actionCheckLoggedIn", null, { root: true });
        console.log({ error });
      });
  },
  getAssignment: async function ({ commit, rootState, state }) {
    // await new Promise((r) => setTimeout(r, 500));
    api
      .getAssignment(rootState.AuthModule.token, state.assignmentToEditId)
      .then((response) => {
        const data = response.data;
        commit("setLastModified", Date.parse(data.last_modified));
        commit("setBundleName", data.bundle_name);
        commit("setAssignmentName", data.assignment_name);
        commit("setSetupCode", data.setup_code);
        commit("setTestsCollection", data.tests_collection);
        commit("setPackageNames", data.package_names);
        commit("setDatasets", []);
        commit("setFileNames", data.datasets ? data.datasets : []);
        if (state.fileNames.length) {
          commit("setFileNames", state.fileNames);
          commit("setIsDatasetsSelected", true);
        } else {
          commit("setIsDatasetsSelected", false);
        }
        if (data.setup_code) {
          commit("setIsSetupSelected", true);
        } else {
          commit("setIsSetupSelected", false);
        }
        if (data.package_names) {
          commit("setIsPackagesSelected", true);
        } else {
          commit("setIsPackagesSelected", false);
        }
      })
      .catch((error) => console.log({ error }));
  },
  createAssignment: async function ({ rootState, dispatch }) {
    // await new Promise((r) => setTimeout(r, 500));
    api
      .createAssignment(rootState.AuthModule.token)
      .then(() => {
        dispatch("getAssignments");
      })
      .catch((error) => console.log({ error }));
  },
  deleteAssignment: function ({ rootState, dispatch }, assignmentId) {
    api
      .deleteAssignment(rootState.AuthModule.token, assignmentId)
      .then(() => {
        dispatch("getAssignments");
      })
      .catch((error) => console.log(error));
  },
  saveAssignment: async function ({ rootState, state, commit, dispatch }) {
    // await new Promise((r) => setTimeout(r, 500));
    api
      .saveAssignment(
        rootState.AuthModule.token,
        state.assignmentToEditId,
        state.bundleName,
        state.assignmentName,
        state.testsCollection,
        state.packageNames,
        state.fileNames,
        state.setupCode
      )
      .then((response) => commit("setLastModified", Date.parse(response.data.last_modified)))
      .catch((error) => {
        dispatch("AuthModule/actionCheckLoggedIn", null, { root: true });
        console.log({ error });
      });
  },
  clearAssignmentStore: async function ({ commit }) {
    commit("setBundleName", "");
    commit("setAssignmentName", "");
    commit("setPackageNames", "");
    commit("setIsSetupSelected", false);
    commit("setIsPackagesSelected", false);
    commit("setIsDatasetsSelected", false);
    commit("setSetupCode", "");
    commit("setDatasets", []);
    commit("setTestsCollection", [{ label: "", visibility: "", code: "" }]);
    commit("setAssignmentToEditId", null);
    commit("setListOfAssignments", []);
  },
};

const mutations = {
  setBundleName: function (state, bundleName) {
    state.bundleName = bundleName;
  },
  setAssignmentName: function (state, assignmentName) {
    state.assignmentName = assignmentName;
  },
  setPackageNames: function (state, packageNames) {
    state.packageNames = packageNames;
  },
  setDatasets: function (state, datasets) {
    state.datasets = datasets;
    if (datasets.length) {
      state.fileNames = [...datasets].map((file) => file.name);
    } else {
      state.fileNames = [];
    }
  },
  setFileNames: function (state, fileNames) {
    state.fileNames = fileNames;
  },

  setIsDatasetsSelected: function (state, isDatasetsSelected) {
    state.isDatasetsSelected = isDatasetsSelected;
  },
  setIsPackagesSelected: function (state, isPackagesSelected) {
    state.isPackagesSelected = isPackagesSelected;
  },
  setIsSetupSelected: function (state, isSetupSelected) {
    state.isSetupSelected = isSetupSelected;
  },
  setSetupCode: function (state, setupCode) {
    state.setupCode = setupCode;
  },
  setTestsCollection: function (state, testsCollection) {
    state.testsCollection = testsCollection;
  },
  setAssignmentToEditId: function (state, assignmentToEditId) {
    state.assignmentToEditId = assignmentToEditId;
  },
  setListOfAssignments: function (state, listOfAssignments) {
    state.listOfAssignments = listOfAssignments;
  },
  setLastModified: function (state, lastModified) {
    state.lastModified = lastModified;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
