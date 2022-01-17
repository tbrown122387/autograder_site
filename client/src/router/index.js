import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import GradingView from "../views/GradingView.vue";
import EditView from "../views/Grading/EditView.vue";
import ListView from "../views/Grading/ListView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import RequestPasswordResetView from "../views/RequestPasswordResetView.vue";
import PasswordResetView from "../views/PasswordResetView.vue";
import AccountView from "../views/AccountView.vue";
import store from "../store/index.js";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/grading",
    name: "Grading",
    redirect: { name: "Edit" },
    component: GradingView,

    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    // component: () =>
    //   import(/* webpackChunkName: "grading" */ "../views/GradingView.vue"),
    children: [
      {
        path: "edit",
        component: EditView,
        name: "Edit",
        beforeEnter: () => {
          if (store.state.AuthModule.isLoggedIn && !store.state.RGradingGradescope.assignmentToEditId) {
            return { name: "List" };
          }
        },
      },
      {
        path: "list",
        component: ListView,
        name: "List",
        beforeEnter: () => {
          if (!store.state.AuthModule.isLoggedIn) {
            return { name: "Edit" };
          }
        },
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
    beforeEnter: () => {
      if (store.state.AuthModule.isLoggedIn) {
        return { name: "Account" };
      }
    },
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterView,
    beforeEnter: () => {
      if (store.state.AuthModule.isLoggedIn) {
        return { name: "Account" };
      }
    },
  },
  {
    path: "/request_password_reset",
    name: "RequestPasswordReset",
    component: RequestPasswordResetView,
    beforeEnter: () => {
      if (store.state.AuthModule.isLoggedIn) {
        return { name: "Account" };
      }
    },
  },
  {
    path: "/password_reset",
    name: "PasswordReset",
    component: PasswordResetView,
    beforeEnter: (to) => {
      if (store.state.AuthModule.isLoggedIn) {
        return { name: "Account" };
      } else if (!("email" in to.query) || !("token" in to.query)) {
        return { name: "Login" };
      }
    },
  },
  {
    path: "/account",
    name: "Account",
    component: AccountView,
    beforeEnter: () => {
      if (!store.state.AuthModule.isLoggedIn) {
        return { name: "Login" };
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(() => store.dispatch("AuthModule/actionCheckLoggedIn"));

export default router;
