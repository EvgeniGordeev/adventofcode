FROM python:3.12.4-slim-bullseye

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get -y install curl

RUN HYPERFINE_VERSION=$(curl -s "https://api.github.com/repos/sharkdp/hyperfine/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+') \
    && curl -Lo hyperfine.deb "https://github.com/sharkdp/hyperfine/releases/latest/download/hyperfine_${HYPERFINE_VERSION}_$(dpkg --print-architecture).deb" \
    && apt-get install -y ./hyperfine.deb \
    && rm -rf hyperfine.deb
