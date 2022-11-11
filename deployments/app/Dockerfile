FROM python:alpine

MAINTAINER Anusha Rao
Label maintainer="Anusha Rao"

ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT

ADD app/ /app

WORKDIR /app

RUN apt-get update

RUN pip install -r ./requirements.txt

EXPOSE 8080

CMD python app.py