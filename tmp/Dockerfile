FROM python:3.8-slim

EXPOSE 8080

COPY . /app

RUN pip3 install flask 

WORKDIR /app

CMD python3 rule-base.py