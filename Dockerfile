FROM python:3.10-buster

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get -y update && \
    apt-get -y install build-essential curl git python-setuptools ruby && \
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install)"

ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin"
RUN brew install hyperfine