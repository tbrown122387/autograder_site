import axios from "axios";

const state = () => ({
  comments: [],
});

const getters = {
  sampleGetter(state) {
    return state.comments;
  },
};

const actions = {
  setComments: function ({ commit }) {
    axios
      .get(process.env.VUE_APP_API_ENDPOINT + "/comments")
      .then((response) => commit("setComments", response.data));
  },
};

const mutations = {
  setComments: function (state, comments) {
    state.comments = comments;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
