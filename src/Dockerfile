# $DEL_BEGIN

# ####### 👇 SIMPLE SOLUTION (x86 and M1) 👇 ########
FROM python:3.8.12-buster

WORKDIR /prod

RUN apt-get update

RUN apt-get install -qq build-essential
RUN apt-get install -qq libfluidsynth-dev
RUN apt-get install -qq libjack-dev
RUN apt-get install -qq libasound2-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api api

CMD uvicorn api.api:app --host 0.0.0.0 --port $PORT
