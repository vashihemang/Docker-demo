# <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="20" height="20" alt="FastAPI">&nbsp;&nbsp;FastAPI Health API with <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="20" height="20" alt="Docker">&nbsp;&nbsp;Docker

A simple REST API built using Python, FastAPI, and Docker.

## Features

- FastAPI application using Python 3.10
- Single GET health-check endpoint
- Dockerized application
- Docker Compose configuration
- Uvicorn ASGI server

## Project Structure

```text
Docker-demo/
│
├── main.py
│
├── fastapi_endpoint/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   │
│   │   │   └── endpoints/
│   │   │       └── users.py
│   │   │
│   │   └── v2/
│   │       │
│   │       └── endpoints/
│   │           └── users.py
│   │
│   └── models/
│       └── users.py
│
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## API Endpoint

**GET /health**

- Default endpint : 
```text 
http://localhost:8000/health
```
- Version 1 endpoint : 
```text 
http://localhost:8000/api/v1/
```
- Version 2 endpoint : 
```text 
http://localhost:8000/api/v2/
```


## Technologies Used

- Python 3.10
- Pydantic
- FastAPI
- Uvicorn
- Docker
- Docker Compose
