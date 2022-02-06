# Backend

This will be updated when more components are added to the backend.

## Overview of Services
### Web Framework
This project uses FastAPI, which can be found [here](https://fastapi.tiangolo.com/). FastAPI primarily is used for RESTful APIs, which is what the backend is. FastAPI has excellent documentation and a thorough user tutorial, which covers all the necessary knowledge to develop this project.

The contents of the API are in the `app` folder. `main.py` is what is run, which looks for endpoints in the `app/api/` folder. An endpoint is simply a function that processes a HTML request. It has an associated URL, such as `/health`. Each request can have headers, request bodies, form data, path parameters, query parameters, and cookie parameters. A request also has an HTTP "verb", such as `GET`, `POST`, and `PUT`. In addition to the endpoints, there are a variety of utility functions. A security module, located in `app/core/`, contains functions that pertain to authentication. `app/crud/` contains utilties for common database operations (CRUD stands for Create, Read, Update, and Delete). `app/models.py` contains the database schemas for tables. `app/schemas/` contains pydantic classes that are used in FastAPI for request bodies. `app/db.py` contains information needed for the app to connect to the database. `app/snippets.py` is used for generating bundles given the autograding information. Dependcies are a powerful FastAPI feature and is located under `app/api/deps.py`. Adhering to DRY, endpoints can reuse the same code known as dependencies.

`app/tests` contains the code to test the endpoints and various utility classes. FastAPI provides a `TestClient` that uses the `requests` library that allows for easy testing of endpoints. `pytest` is the testing framework used and it runs the tests for any file in the `tests` folder that is prefixed with `test_`. Inside any file prefixed with `test_`, it runs any function prefixed with `test_`. In those functions, if an exception occurs (that is not expected), then the test will result in a fail. `pytest` also includes a concept known as `fixtures` which are located in `app/tests/conftest.py`. Tests should follow an Arrange, Act, Assert design pattern. In this pattern, many tests have similar Arrange steps, where tests have to set up some database connection or initalize some data. The repeated code is the fixture, which can be added as a parameter onto the actual test function itself. 


To run tests without anything running (recommended)
```
$ ./scripts/run_tests_server.sh
```

To run tests once the development server is run:
```
$ docker exec grading-site-api python3 -m pytest
```
> Some tests were not written to be run repeatedly, e.g. creating users with the same email twice will result in a database integrity error. Because of this, it is recommended to delete all resources (`docker compose down`) before re-running any tests.

### Authentication/Security
This website can save user assignments by making use of user accounts. For these user accounts to function, several endpoints are located in the `api/api_v*/endpoints/auth.py` file that assist with creating, deleteing, and modifying user accounts. A token based authentication method is used for validating users when accessing private resources. This means a token is given to the user when they log in with an certain expiration time. The browser stores this token, so any time a request is made to a protected endpoint, such as `/account`, the browser sends the token with the request, which the server then processes and validates. If valid, the server knows who the user is. If the token is expired or invalid, the server returns an authentication error.

The web framework (FastAPI), handles a lot of the implementation and has a detailed user guide on this concept [here](https://fastapi.tiangolo.com/tutorial/security/). For more information about the tokens, see [JSON Web Tokens (JWT)](https://jwt.io/introduction). 

### Database
We are using a PostgreSQL relational database for this project. 

### ORM
ORM stands for Object Relational Mapper. ORM's help translate database tables into (in this case) Python objects. Instead of writing SQL directly, ORM's allow Python syntax to build tables and generate queries and allow developers to generally adhere to Object Oriented Programming principles better. In addition, it allows for much faster development because IDE's are able to debug and provide code completion.

In this project [SQLModel](https://sqlmodel.tiangolo.com/) is used. SQLModel uses SQLAlchemy under the hood and is written by the same author of FastAPI, so there are several features that allow FastAPI and SQLModel to work well together. SQLModel greatly simplifies non complex database operations, while still allowing raw SQLAlchemy to be used easily.

### Database Migrations
Database Migrations are needed whenever database schemas are altered, i.e. a table/column is added/removed/modified. There needs to be a strict guide for the database to transfer existing data into a new schema. For this purpose, we are using [Alembic](https://alembic.sqlalchemy.org/en/latest/). Alembic works with SQLAlchemy and, since SQLModel uses SQLAlchemy under the hood, can be used here.

Revisions are `*.py` files under `alembic/versions/` and are autogenerated based on the models in `app/models.py`

```console
$ docker exec -it grading-site-api bash
$ python3 -m alembic revision --autogenerate -m "your message"
$ python3 -m alembic history
$ python3 -m alembic upgrade head
$ python3 -m alembic downgrade/upgrade +1/-1
```
> Migrations are automatically run when using `docker compose up`

## Development Setup
The development version of the backend can be run with `docker compose up server` in the root directory. If there is a change to the `Dockerfile` or `requirements.txt`, then run `docker compose up --build server`. Since the database is listed as a dependency, the database also starts up.

pgAdmin is also included to view the development database and debug.

```console
$ docker compose up server pgadmin
```

Then visit `http://localhost:5050`. The username and password are located in the `.env` file in the root directory. Then, "Add New Server". "Name" can be anything, then under the "Connection" tab, put `postgres` for Host Name and the appropriate username and password from the `.env` file.


## Deployment
The backend is deployed using Heroku. The PostgreSQL database is also on Heroku.

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
- GitHub Actions CI
- Auto deploy from GitHub to Heroku
  - Heroku can connect to a Github repository and auto deploy when a new commit is pushed.
  - This is a little complicated in this case because we want to deploy a subfolder
  - Also allows less control when deploying changes for major versions
  - https://stackoverflow.com/questions/39197334/automated-heroku-deploy-from-subfolder - Heroku Buildpack needed
- Multiple Workers in Deployment