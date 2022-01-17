<template>
  <div class="p-6 mx-auto mt-5 border-2 shadow-lg md:w-9/12 xl:max-w-4xl">
    <div>
      <button class="p-2 font-bold text-white bg-red-700 rounded shadow" @click="submitLogOut">Log Out</button>
    </div>
    <div>
      {{ email }}
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  name: "AccountView",
  components: {},
  data: function () {
    return {};
  },
  methods: {
    ...mapActions("AuthModule", ["actionLogOut", "actionCheckLoggedIn"]),
    submitLogOut() {
      this.actionLogOut().then(() => {
        this.$router.push({ name: "Login" });
      });
    },
  },
  computed: {
    ...mapState("AuthModule", ["email", "isLoggedIn"]),
  },
};
</script>
