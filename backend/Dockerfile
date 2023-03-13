FROM python:3.8-slim AS compile-image

ARG DOCKER_PROVISION_PATH

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y build-essential

RUN python3.8 -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip3.8 install --upgrade pip
RUN pip3.8 install --no-cache -r requirements.txt

FROM python:3.8-slim AS build-image

COPY --from=compile-image /opt/venv /opt/venv

WORKDIR /app

# libraries required by OpenCV
RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
    libfluidsynth-dev \
    libasound2-dev \
    libjack-dev \
    && apt-get remove --purge --auto-remove -y && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

# You can add --port $PORT if you need to set PORT as a specific env variable
CMD uvicorn fast_api.api:app --host 0.0.0.0 --port $PORT
