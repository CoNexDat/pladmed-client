FROM alpine:3.7

COPY ./scamper ./scamper
COPY ./docker-entrypoint.sh .
COPY ./src/requirements.txt .

# Register daily cron job for client time synchronization
ARG SYNC_TIME
ENV SYNC_TIME_VAR=${SYNC_TIME}
RUN mkdir /etc/cron.d
RUN echo "Daily sync at UTC hour: ${SYNC_TIME_VAR}"
COPY ./time-sync/crontab /etc/cron.d/timesync
RUN sed -i "s/__SYNC_TIME__/${SYNC_TIME_VAR}/g" /etc/cron.d/timesync
RUN chmod 0644 /etc/cron.d/timesync
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/timesync

# Install client app's Python modules and their dependencies
RUN apk add gcc g++ libffi-dev musl-dev zlib-dev linux-headers make bind-tools \
    && cd scamper && ./configure && make && make install

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install -r requirements.txt
RUN chmod -R +x scamper/

# Install faketime in order to set the container time without affecting the host
WORKDIR /
RUN wget https://github.com/wolfcw/libfaketime/archive/master.tar.gz
RUN tar -xzf master.tar.gz
WORKDIR /libfaketime-master/src
RUN make install

# Remove dependencies which will not be needed in runtime
RUN rm -rf /libfaketime/master
RUN apk del gcc g++ libffi-dev musl-dev zlib-dev linux-headers make

ENV HOME=/src
WORKDIR $HOME

ENTRYPOINT ["/bin/sh"]
