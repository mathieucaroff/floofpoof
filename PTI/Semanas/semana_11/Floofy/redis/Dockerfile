FROM redis:6
RUN mkdir /redis
WORKDIR /redis
COPY redis.conf /redis/
CMD redis-server redis.conf