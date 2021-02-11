FROM alpine:3.7

COPY ./scamper ./scamper
COPY ./src/requirements.txt .

RUN apk add gcc g++ libffi-dev musl-dev zlib-dev linux-headers make bind-tools \
    && cd scamper && ./configure && make && make install \
    && apk del gcc g++ libffi-dev musl-dev zlib-dev linux-headers make

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install -r requirements.txt

RUN chmod -R +x scamper/

ENV HOME=/src
WORKDIR $HOME

ENTRYPOINT ["/bin/sh"]
