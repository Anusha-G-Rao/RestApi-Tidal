FROM python:3.8.10-alpine

MAINTAINER Anusha Rao

ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT

WORKDIR /app

COPY ./app/requirements.txt .
RUN apk add build-base
RUN pip install -r requirements.txt

COPY . .
RUN python test.py || exit 1
CMD ["python", "app.py"]

