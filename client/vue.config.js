module.exports = {
  transpileDependencies: ["vuetify"],
  pages: {
    index: {
      entry: "src/main.js",
      title: "Autograding Bundler",
    },
  },
  publicPath: "/",
  // publicPath: process.env.NODE_ENV === "production" ? "/autograder_site/" : "/",
};
