# Backend Service (FastApi)


## Setup Steps

### 1. Clone the Repository

Clone the repository to your local machine and navigate into the project directory:

```sh
git clone https://github.com/sundar68/filemanager.git
cd filemanager
```

## Running backend service locally

### Actiate conda or python virtual environment and run following commands.

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 3210
```

## Run Minio server and PostgreSql

```bash
docker pull minio/minio
docker pull postgres:16
docker-compose up -d
```
# create a bucket in minio with name 'filemanager'
# Get the Access Id and Secret key and set it in .env file



## Postgres Commands

```bash
psql -U postgres -h localhost
CREATE DATABASE typeface;
\c typeface;

CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    size INTEGER NOT NULL,
    url TEXT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    storage_type VARCHAR NOT NULL
);
```

# Frontend Service (React & TypeScript)

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

 [Watch the demo video]

## 📽️ Watch the demo video 
## Drive link for demo : https://drive.google.com/file/d/12MBhYAbkPxnt4uzMfomW6JLvr5PFc9jz/view?usp=sharing