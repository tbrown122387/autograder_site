import axios from "axios";

const state = () => ({
  bundleName: "",
  assignmentName: "",
  packageNames: "",
  numberOfTests: 1,
  datasets: [],
  labels: [],
  visibilities: [],
  codes: [],
});

const getters = {};

const actions = {
  setBundleName: function ({ commit }, bundleName) {
    commit("setBundleName", bundleName);
  },
  setAssignmentName: function ({ commit }, assignmentName) {
    commit("setAssignmentName", assignmentName);
  },
  setPackageNames: function ({ commit }, packageNames) {
    commit("setPackageNames", packageNames);
  },
  setDatasets: function ({ commit }, datasets) {
    commit("setDatasets", datasets);
  },
  setLabels: function ({ commit }, labels) {
    commit("setLabels", labels);
  },
  setVisibilities: function ({ commit }, visibilities) {
    commit("setVisibilities", visibilities);
  },
  setCodes: function ({ commit }, codes) {
    commit("setCodes", codes);
  },
  incrementNumberOfTests: function ({ commit, state }) {
    commit("setNumberOfTests", state.numberOfTests + 1);
  },
  decrementNumberOfTests: function ({ commit, state }) {
    commit("setNumberOfTests", state.numberOfTests - 1);
    commit("setLabels", state.labels.slice(0, state.numberOfTests));
    commit("setVisibilities", state.visibilities.slice(0, state.numberOfTests));
    commit("setCodes", state.codes.slice(0, state.numberOfTests));
  },
  setComments: function ({ commit }) {
    axios
      .get(process.env.VUE_APP_API_ENDPOINT + "/comments")
      .then((response) => commit("setComments", response.data));
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
  },
  setLabels: function (state, labels) {
    state.labels = labels;
  },
  setVisibilities: function (state, visibilities) {
    state.visibilities = visibilities;
  },
  setCodes: function (state, codes) {
    state.codes = codes;
  },
  setNumberOfTests: function (state, numberOfTests) {
    state.numberOfTests = numberOfTests;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
