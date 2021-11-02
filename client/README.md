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

`App.vue` contains the navigation bar at the top, an empty footer, and the `<router-view>`. This `<router-view>` is defined in `src/router/index.js`. Each url is given a "View" from `src/views/`. For `/` (root of the website, i.e. `localhost:8080/` when running locally), `src/views/HomeView.vue` is what is displayed. The "Home" view can also use components which are defined in the `src/components/` folder. Components are what makes development fast and easy, because pieces can be generalized and reused for different pages.

> The following paragraph does not exist in the current version. However, `src/views/GradingView` contains an example of a POST HTTP request to upload the files and grading data.
 
The "About" view, whose code is in `src/views/About.vue` demonstrates how to call an API from the frontend. When a button is clicked, a function is run, which in this case uses the `axios` HTTP client to make a request to the backend. The reactive value `text` is then set to the response of the API call.

`package.json` details all the packages needed to run and build this website. The `scripts` section has common commands, so they are easier to run for the developer. `npm run serve` is to launch the developement server. `npm run build` builds a static production version of the site into the `dist/` directory. Then, an HTTP Server can be used to host the files. `python3 -m http.server` is an example of a HTTP Server (for development).

## Deployment

The frontend is deployed using Github Pages.

The development version is used when running `docker compose up` as stated in the `README.md` of the root of the repo. The development version is useful for development (obviously) as it hot reloads on changes and contains debugging utilities. However, it is far slower, so the website needs to be built into the production version for better stability and latency.

Github Pages deploys whatever is in the `gh-pages` branch in the main repo (https://github.com/tbrown122387/autograder_site/tree/gh-pages). Since `npm run build` builds a static production version of the site into the `dist/` directory, we can directly push the `client/dist/` directory to the `gh-pages` branch.
```console
$ git subtree push --prefix client/dist upstream gh-pages
```

> `upstream` is the shorthand name for remote branch of the main repository. It may be called something else, so use the following command to check what it is.
>    ```console
>    $ git remote -v
>    > upstream	git@github.com:tbrown122387/autograder_site.git (fetch)
>    > upstream	git@github.com:tbrown122387/autograder_site.git (push)
>    ```
> It is very important to ensure that your configuration is correct for these commands.

In cases where multiple users are deploying, sometimes the `gh-pages` branch can have merge conflicts. While these will be resolved in the main development branch on Github, the `gh-pages` branch will not get those updates. Therefore, use the following code to force push any changes to deploy.

```console
$ git push upstream `git subtree split --prefix client/dist main`:gh-pages --force
```
