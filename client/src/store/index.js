import Vue from "vue";
import Vuex from "vuex";
import General from "./modules/general";
import RGradingGradescope from "./modules/rgrading_gradescope";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    General,
    RGradingGradescope,
  },
});
