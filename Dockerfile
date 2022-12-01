FROM python:3.11.0-slim-buster

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get -y install curl

RUN HYPERFINE_VERSION=$(curl -s "https://api.github.com/repos/sharkdp/hyperfine/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+') \
    && curl -Lo hyperfine.deb "https://github.com/sharkdp/hyperfine/releases/latest/download/hyperfine_${HYPERFINE_VERSION}_amd64.deb" \
    && apt-get install -y ./hyperfine.deb \
    && rm -rf hyperfine.deb

RUN hyperfine --version

#RUN apt-get -y update && \
#    apt-get -y install build-essential curl git python-setuptools ruby && \
#    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Linuxbrew/install/master/install)"


#ENV PATH="$PATH:/home/linuxbrew/.linuxbrew/bin"
#RUN brew install hyperfine