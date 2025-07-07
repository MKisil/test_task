# Simple File System

## Features

- Create, read, update, delete files
- List files with optional sorting(modified, size)
- Get file metadata
- List files in a directory

## Setup

You can set up the project locally or with Docker.

```bash
poetry install
```
```bash
poetry shell
```
```bash
python manage.py runserver
```

```bash
docker build -t test-task .
```
```bash
docker run -p 8080:8080 test-task
```
