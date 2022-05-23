FROM python:3.11-rc-slim-bullseye

RUN pip3 install pymongo flask

ADD . /www

WORKDIR /www

CMD ["python3", "main.py"]
