import axios from "axios";
import { api } from "../api";
import router from "../router";
import { saveLocalToken, getLocalToken, removeLocalToken } from "../utils";

const state = () => ({
  email: "",
  token: "",
  isLoggedIn: false,
  isErrorLoggingIn: false,
  isErrorRegistering: false,
});

const getters = {};

const actions = {
  async actionGetToken({ commit, dispatch }, email, password) {
    try {
      const response = await api.logInGetToken(email, password);
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
      }
      commit("commitSetIsLoggedIn", true);
      commit("commitSetIsErrorLoggingIn", false);
      commit("commitSetEmail", email);
      dispatch("actionLogIn");
    } catch (error) {
      console.log("There was an error in logging in");
      commit("commitSetIsErrorLoggingIn", true);
      commit("commitSetEmail", "");
    }
  },
  async actionRegister({ commit }, email, password) {
    try {
      await api.registerAccount(email, password);
      commit("commitSetIsErrorRegistering", false);
      commit("commitSetIsErrorLoggingIn", false);
    } catch (error) {
      console.log("There was an error in registering");
      commit("commitSetIsErrorRegistering", true);
    }
  },
  async actionCheckLoggedIn({ commit, state, dispatch }) {
    let token = state.token;
    if (!token) {
      const localToken = getLocalToken();
      if (localToken) {
        commit("commitSetToken", localToken);
        token = localToken;
      }
    }
    if (token) {
      try {
        const response = await api.getAccount(token);
        console.log(JSON.stringify(response));
        dispatch("actionLogIn");
      } catch (error) {
        dispatch("actionLogOut");
      }
    } else {
      dispatch("actionLogOut");
    }
  },
  async actionLogIn() {
    if (
      router.currentRoute.path === "/login" ||
      router.currentRoute.path === "/register"
    ) {
      router.push({ path: "account" });
    }
  },
  async actionLogOut({ commit }) {
    removeLocalToken();
    commit("commitSetEmail", "");
    commit("commitSetToken", "");
    commit("commitSetIsLoggedIn", false);
    router.push({ path: "login" });
  },
  setComments: function ({ commit }) {
    axios
      .get(process.env.VUE_APP_API_ENDPOINT + "/comments")
      .then((response) => commit("setComments", response.data));
  },
};

const mutations = {
  commitSetToken(state, token) {
    state.token = token;
  },
  commitSetIsLoggedIn(state, isLoggedIn) {
    state.isLoggedIn = isLoggedIn;
  },
  commitSetEmail(state, email) {
    state.email = email;
  },
  commitSetIsErrorLoggingIn(state, isErrorLoggingIn) {
    state.isErrorLoggingIn = isErrorLoggingIn;
  },
  commitSetIsErrorRegistering(state, isErrorRegistering) {
    state.isErrorRegistering = isErrorRegistering;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
