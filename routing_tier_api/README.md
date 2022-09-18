# routing-tier-api

Project for router tier

[![Built with Cookiecutter](https://img.shields.io/badge/build%20with%20Cookiecutter%20FastAPI-purple)](https://github.com/sgg10/cookiecutter-fastapi)

# Table of contents
1. [Prerequisites](#prerequisites)
2. [Installing](#installing)
3. [Project structure](#structure)
4. [Environment variables](#environment)
5. [How to use](#howto)

# Prerequisites <a name="prerequisites"></a>

- It is necessary to have docker and docker compose installed (for the latest versions of docker, only this is enough since compose is integrated).

- It is recommended to have Python3.9 installed to be able to handle dependencies within the text editor and use features such as autocomplete.

# Installing <a name="installing"></a>
The first step to start the project is the building.

```bash
docker-compose build
```
```bash
docker compose build # For the latest versions
```

The env variables are located inside the .envs/ directory where you must locate the environment to which you are going to assign variables, they are divided into multiple files as appropriate.

```bash
docker-compose up
```
```bash
docker compose up # For the latest versions
```

# Project structure <a name="structure"></a>
```
ds_node_silin_api
├── app                                   // FastAPI App directory
│   ├── api                               // Routers that make up the API
│   │   ├── models.py                     // Models for router
│   │   └── router.py                     // Router endpoint registry
│   ├── core                              // Core of app
│   │   ├── config.py                     // Global configuration for app
│   │   └── settings                      // Settings by ENV module
│   │       ├── base.py                   // Base global setting for app
│   │       ├── local.py                  // Setting for local environment
│   │       └── production.py             // Setting for production environment
│   ├── node                              // Node module
│   │   ├── node.py                       // Node class
│   │   └── status.py                     // Node health status check
│   ├── works                             // Works Module
│   │   ├── initialization.py             // Global Node initialization
│   │   ├── redistribution.py             // Redistribution works (for nodes up or down)
│   │   ├── send_action.py                // Global action sender to nodes
│   │   └── tasks                         // Tasks submodule
│   │       ├── calculate_distribution.py // Calcs for determinate node distributions
│   │       └── key_identifier.py         // Indetify node target in order to key
│   └── main.py                           // Main app file
├── logs                                  // Logs Directory
├── docker                                // Docker configuration
│   ├── local
│   │   └── fastapi
│   │       ├── Dockerfile                // Docker file to local environment
│   │       └── start                     // Script to start fastapi service
│   └── production
│       └── fastapi
│           └── start                     // Script to start fastapi service
├── .envs                                 // Sensitive variables for each environment
│   └ .app
├── requirements                          // Recursive requirements
│   ├── base.txt                          // Base app requirements
│   ├── local.txt                         // Local requirements
│   └── production.txt                    // Production requirements
├── tests                                 // Test Directory
│   └── test_sample.py
├── .gitignore
├── .dockerignore
├── .editorconfig
├── .docker-compose.yml
├── Dockerfile                            // Docker file to deploy
├── setup.cfg
├── pytest.ini                            // PyTest configuration file
└── README.md                             // This file
```

# Environment variables <a name="environment"></a>
`ENV` in variable name means that it is replaced in the file according to the environment

|Name|Type|File|Sensitive|Description|
|----|----|----|---------|-----------|
|ENV|STR|.envs/.app|FALSE|`local` or `prod` environment|
|PORT|INT|.envs/.app|FALSE|Port on which the microservice runs|
|SERVICE_NAME|STR|.envs/.app|FALSE|Name of microservice|
|ALLOWED_ORIGINS|LIST|.envs/.app|FALSE|CORS Origins|
|NODE_HOSTS|LIST|.envs/.app|FALSE|Node hosts to connect|

# How to use <a name="howto"></a>

```bash
docker-compose build
```
After, you can use the following commands to start
```bash
docker-compose up
# Or docker-compose up -d to run in background
```
## Tests
```bash
docker-compose run --rm fastapi pytest
```

## SAST
Run to check static application security testing
```bash
docker-compose run --rm fastapi bandit -r app
```

## Type Checks

Running type checks with mypy:

```bash
docker-compose run --rm fastapi mypy ds_node_silin_api
```

## Test Coverage
```bash
docker-compose run --rm fastapi coverage run -m pytest
docker-compose run --rm fastapi coverage html
```
After, open `htmlcov/index.html`.

## Flake8
```bash
docker-compose run --rm fastapi flake8 path/to/code/
```
