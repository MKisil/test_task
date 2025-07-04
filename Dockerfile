FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=0

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
