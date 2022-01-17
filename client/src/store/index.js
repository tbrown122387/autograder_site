import { createStore } from "vuex";
import RGradingGradescope from "./rGradingModule.js";
import AuthModule from "./authModule.js";

export default createStore({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    RGradingGradescope,
    AuthModule,
  },
  strict: process.env.NODE_ENV !== "production",
});
