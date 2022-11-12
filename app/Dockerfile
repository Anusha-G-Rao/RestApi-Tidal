FROM python:3.8.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN apk add build-base
RUN pip install -r requirements.txt

COPY . .
RUN python test.py || exit 1
CMD ["python", "app.py"]

