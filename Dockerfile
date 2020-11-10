FROM alpine:3.7

COPY ./src .

RUN apk add gcc g++ libffi-dev musl-dev zlib-dev linux-headers make\
    && cd scamper && ./configure && make && make install \
    && apk del gcc g++ libffi-dev musl-dev zlib-dev linux-headers make

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install scamper-pywarts

CMD ["python", "main.py"]