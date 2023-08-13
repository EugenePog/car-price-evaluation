FROM python:3.10.12-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["app.py", "./"]
COPY ["templates/index.html", "./templates/"]
COPY ["mlflow.db", "./"]
COPY ["mlruns/", "./mlruns/"]

RUN mkdir models

EXPOSE 5011

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:5011", "app:app" ]
