import { api } from "../api";
import { saveLocalToken, getLocalToken, removeLocalToken } from "../utils";

const state = () => ({
  email: "",
  token: "",
  isLoggedIn: false,
  isErrorLoggingIn: false,
  errorLoggingIn: {},
  isErrorRegistering: false,
});

const getters = {};

const actions = {
  async actionGetToken({ commit, dispatch }, email, password) {
    return api
      .logInGetToken(email, password)
      .then((response) => {
        const token = response.data.access_token;
        if (token) {
          saveLocalToken(token);
        }
        commit("commitSetToken", token);
        dispatch("actionLogIn", email);
      })
      .catch((error) => {
        commit("commitSetIsErrorLoggingIn", true);
        commit("commitSetErrorLoggingIn", { error });
        commit("commitSetEmail", "");
      });
  },
  async actionRegister({ commit }, email, password) {
    try {
      await api.registerAccount(email, password);
      commit("commitSetIsErrorRegistering", false);
      commit("commitSetIsErrorLoggingIn", false);
    } catch (error) {
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
      // token in local storage or vuex store
      try {
        const response = await api.getAccount(token);
        dispatch("actionLogIn", response.data.email);
      } catch (error) {
        dispatch("actionLogOut");
      }
    } else {
      dispatch("actionLogOut");
    }
  },
  async actionLogIn({ commit }, email) {
    commit("commitSetIsLoggedIn", true);
    commit("commitSetIsErrorLoggingIn", false);
    commit("commitSetErrorLoggingIn", {});
    commit("commitSetEmail", email);
  },
  async actionLogOut({ commit, state, dispatch }) {
    removeLocalToken();
    commit("commitSetEmail", "");
    commit("commitSetToken", "");
    if (state.isLoggedIn) {
      dispatch("RGradingGradescope/clearAssignmentStore", null, { root: true });
    }
    commit("commitSetIsLoggedIn", false);
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
  commitSetErrorLoggingIn(state, errorLoggingIn) {
    state.errorLoggingIn = errorLoggingIn;
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
