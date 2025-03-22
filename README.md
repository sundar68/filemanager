# Frontend Service (React & TypeScript)

This repository contains the Docker setup for a frontend service built with React and TypeScript. The application is built using Node.js 22 (managed via NVM) and served using Nginx on port **3210**.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

## Setup Steps

### 1. Clone the Repository

Clone the repository to your local machine and navigate into the project directory:

```sh
git clone https://github.com/sundar68/filemanager
cd filemanager
```

## Running backend service locally

### Actiate conda or python virtual environment and run following commands.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 3210
```

## Run Minio server

```bash
docker pull minio/minio
docker pull postgres:16
docker-compose up -d
```


## Running Frontend service locally

# Use node version 22
```bash
nvm use v22
```

## Install packages and run
```bash
npm i
npm run dev
```
