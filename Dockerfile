FROM python:3.12

WORKDIR /bot

COPY . .

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "bot.py" ]