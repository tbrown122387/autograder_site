# Backend

This will be updated when more components are added to the backend.

## Details
We are using FastAPI, which can be found [here](https://fastapi.tiangolo.com/)

## Deployment
The backend is deployed using Heroku.


```console
$ heroku git:remote -a autograder-site
```

```console
$ git subtree push --prefix server heroku main
```

## TODO
1. Add database integration (PostgreSQL)
2. Refactor project into modules