# Simple File System

## Features

- Create, read, update, delete files
- List files with optional sorting(name, size)
- Search files by name or content
- Get file metadata
- List files in a directory

## Search Performance

- **Search by filename:** O(1) due to the use of a dictionary for filename indexing (case sensitive).
- **Search by content:** O(n), where n is the number of files, as it checks each file content (not case sensitive).  
  I thought about indexing each word, but it would not support phrase searches.


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


## Running unit tests

Run unit tests with: 
```bash
python manage.py test
```
