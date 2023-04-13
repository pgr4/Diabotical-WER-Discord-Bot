FROM python:3.10

ENV DISCORD_TOKEN=MTAzNjgzNzQ1ODYyNjc1NjYyOA.GQc36d.v98n9IJZe8fjI2mL4bNZWTzLjacof1YXKzy_VU

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

VOLUME [ "/data" ]

COPY . .

CMD [ "python", "main.py" ]