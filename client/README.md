# Frontend

This folder contains the code for the frontend portion of the website.

## Technical Details
Vue 2 is being used with the following integrations/plugins

> Vue 2 is being used instead of Vue 3 because Vuetify has not yet updated.

1. [Vuetify](https://vuetifyjs.com/en/)
2. [Vuex](https://vuex.vuejs.org/)
3. [Vue Router](https://router.vuejs.org/)

## How it works

All the development code is located in the `src` folder. To use the website in production, you must first build the code into a production version. Inside `public/index.html`, all the built code goes inside the `div` tag with an id of `app`. This is defined in `src/main.js`, where the mount point is `"#app"`. `src/main.js` also shows that `App` from `src/App.vue` is the website itself.

`App.vue` contains the navigation bar at the top, an empty footer, and the `<router-view>`. This `<router-view>` is defined in `src/router/index.js`. Each url is given a "View" from `src/views/`. For `/` (root of the website, i.e. `localhost:8080/` when running locally), `src/views/Home.vue` is what is displayed. The "Home" view can also use components which are defined in the `src/components/` folder. Components are what makes development fast and easy, because pieces can be generalized and reused for different pages.

The "About" view, whose code is in `src/views/About.vue` demonstrates how to call an API from the frontend. When a button is clicked, a function is run, which in this case uses the `axios` HTTP client to make a request to the backend. The reactive value `text` is then set to the response of the API call.
