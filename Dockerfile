FROM python:3.8

WORKDIR /app


RUN pip install pipenv

COPY ./Pipfile ./
COPY ./Pipfile.lock ./

RUN pipenv install --deploy

ENV FLASK_APP=src/server.py

COPY ./ ./

EXPOSE 8080

CMD ["pipenv", "run", "waitress-serve", "src.server:app"]
