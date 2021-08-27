FROM python:3.9.4-buster

ENV PATH = "/opt/venv/bin:$PATH"

COPY . .

COPY requirements.txt requirements.txt

RUN apt-get install git


RUN pip install --no-cache-dir --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt
