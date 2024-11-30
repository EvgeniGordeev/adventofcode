FROM python:3.13.0-slim-bullseye

RUN apt-get update -y && apt-get -y install curl
# pipenv install bloats this image by 30MB+
#RUN pip install --upgrade pip && pip install pipenv==2024.4.0

#COPY Pipfile Pipfile.lock ./
COPY requirements.txt ./
#RUN pipenv install --system --deploy --ignore-pipfile && pip uninstall -y pipenv
RUN pip install -r requirements.txt

RUN HYPERFINE_VERSION=$(curl -s "https://api.github.com/repos/sharkdp/hyperfine/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+') \
    && curl -Lo hyperfine.deb "https://github.com/sharkdp/hyperfine/releases/latest/download/hyperfine_${HYPERFINE_VERSION}_$(dpkg --print-architecture).deb" \
    && apt-get install -y ./hyperfine.deb \
    && rm -rf hyperfine.deb
