FROM python:3.9-slim-buster

WORKDIR /app

EXPOSE 5000

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]
