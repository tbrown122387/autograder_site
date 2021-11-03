# Backend

This will be updated when more components are added to the backend.

## Details
We are using FastAPI, which can be found [here](https://fastapi.tiangolo.com/)

## Deployment
The backend is deployed using Heroku.

Our current setup uses the Heroku CLI to deploy. Here are some steps to set that up for the first time.
```console
$ heroku login
$ heroku git:remote -a autograder-site
```
To verify the correct remote repositories were added, run the following
```console
$ git remote -v
> heroku https://git.heroku.com/autograder-site.git (fetch)
> heroku https://git.heroku.com/autograder-site.git (push)
```

Heroku deploys whatever code is present in the `main` branch on the git repository on Heroku. Therefore, to deploy, we need to push code from our local repository to the Heroku repository. Since all the server code is located in `server/`, we can run the following command to push just the `server/` folder to the `main` branch of the Heroku remote repository.

```console
$ git subtree push --prefix server heroku main
```

In cases where multiple users are deploying, sometimes the remote Heroku repository can have merge conflicts. While these will be resolved in the main development branch on Github, the Heroku repository will not get those updates. Therefore, use the following code to force push any changes to deploy.

```console
$ git push heroku `git subtree split --prefix server main`:main --force
```

These are some helpful CLI commands that can be used to monitor Heroku services.
```console
$ heroku apps
$ heroku config
$ heroku logs --tail
$ heroku psql
> \d
```

The `Procfile` details the running configuration for Heroku.

# TODO:
- Auto deploy from Heroku
  - Heroku can connect to a Github repository and auto deploy when a new commit is pushed.
  - This is a little complicated in this case because we want to deploy a subfolder
  - Also allows less control when deploying changes for major versions
  - Needs to be combined with CI Testing Suite to ensure build failures don't occur
  - https://stackoverflow.com/questions/39197334/automated-heroku-deploy-from-subfolder - Heroku Buildpack needed
- Multiple Workers in Deployment