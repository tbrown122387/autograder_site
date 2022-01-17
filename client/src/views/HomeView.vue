<template>
  <div class="p-6 mx-auto mt-5 border-2 shadow-lg md:w-9/12 xl:max-w-4xl">
    <div class="text-xl font-bold">Autograding Bundler</div>
    <div>
      <p>
        This site helps you make "bundles" for autograding. Currently, we
        support the following:
      </p>
      <ul class="list-inside list-square">
        <li>Autograding in Gradescope with R</li>
      </ul>
      <br />
      <p>These are some more features we have planned:</p>
      <ul class="list-inside list-square">
        <li>Autograding in Gradescope with Python</li>
        <li>Autograding in Gradescope with Python via OtterGrader</li>
        <li>Autograding Locally with R</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script>

<style>
</style>
