# Autograder Generator Site (version 2!)

A website that helps instructors use autograding tools for their courses.

## Thanks

This work is supported by [The Learning Design & Technology team](https://learningdesign.as.virginia.edu/) at the University of Virginia.

## Getting Started
```console
$ git clone https://github.com/tbrown122387/autograder_site.git
```

### Development with Docker
#### Prerequisites
1. Install Docker on your system. The getting started guide is located [here](https://www.docker.com/get-started).
2. Verify Docker is installed with `docker --version`

#### Guide
> This may not work on Windows, let us know if you encounter any issues
> 
For first time setup or if there are changes to `requirements.txt` or `package.json`:

```console
$ docker compose up --build
```

For any other time:

```console
$ docker compose up
```
Note that you may need `docker-compose` instead of `docker compose`.

Then, navigate to `localhost:8080` to see the website. When making changes to either the client or the API, hot-reloading is enabled, so the page will update whenever a change is saved.

If you want to fully close the website and delete associated data:
```
$ docker compose down
```


#### Details
`docker-compose.yml` defines all the services needed. Currently, there is a client that is the frontend, a server that is the backend, a PostgreSQL database, and PGAdmin for monitoring the development database. The `Dockerfile` in the client and server folder shows how the container is built for each service.

## TODO
- [x] Backend - Refactor into Modules
- [x] Backend - Authentication
- [x] Backend - Testing
- [x] Support for Setup Code
- [x] Support for .Rmd
- [ ] Backend - GitHub Actions for CI
- [ ] Frontend - Testing
- [ ] Frontend - GitHub Actions for CI
- [ ] Zip on Frontend
- [ ] GitHub Actions for CD
