FROM python:3.10

ARG DISCORD_TOKEN
ENV DISCORD_TOKEN=${DISCORD_TOKEN}

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

VOLUME [ "/data" ]

COPY . .

CMD [ "python", "main.py" ]