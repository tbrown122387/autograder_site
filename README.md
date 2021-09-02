# Autograder Generator Site (version 2!)

A website that helps instructors use autograding tools for their courses.

## Thanks

This work is supported by [The Learning Design & Technology team](https://learningdesign.as.virginia.edu/) at the University of Virginia.

## Getting Started
```console
$ git clone https://github.com/tbrown122387/autograder_site.git
```

There are two primary ways to launch the development version of the website, using Docker or manually configuring each service.

### With Docker
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

Then, navigate to `localhost:8080` to see the website. When making changes to either the client or the API, hot-reloading is enabled, so the page will update whenever a change is saved.

If you want to fully close the website and delete associated data:
```
$ docker compose down
```


#### Details
`docker-compose.yml` defines all the services needed. Currently, there is a client that is the frontend and a server that is the backend. The `Dockerfile` in each folder shows how the container is built.

### Manual Configuration
Prerequisites
1. `node` which can be found [here](https://nodejs.org/en/download/)
2. Verify `npm` is installed with `npm --version` (`npm` comes bundled with `node`)
3. `python` which can be found [here](https://www.python.org/)
4. Verify `python` is installed with `python3 --version`


#### Guide
1. Install the necessary development packages for the frontend
```console
$ cd client
$ npm install
```
2. Create a virtual env for python and install the necessary packages
```console
$ cd server
$ python3 -m venv venv # creates a virtual environment with the name 'venv'
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

3. Start the Vue development server
```console
$ cd client
$ npm run serve
```

4. Start the Python development server in a different terminal window
```console
$ cd server
$ source venv/bin/activate # needed if new terminal session
$ python3 main.py
```