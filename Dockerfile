FROM python:alpine

COPY . ./app

WORKDIR /app

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt;

ENTRYPOINT [ "python" ]

CMD ["main.py"]
