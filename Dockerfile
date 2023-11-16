FROM python:3.6-slim-buster



# 更新包信息并安装依赖
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT 5000
ENV USERNAME admin
ENV PASSWORD admin
ENV OPENSSL_CONF /etc/ssl/
ENV DB_NAME web
ENV DB_USER root
ENV DB_PASSWORD zhou2283724797
ENV DB_HOST localhost
ENV DB_PORT 3306

COPY . /app

WORKDIR /app

RUN set -x; buildDeps='wget build-essential' \
&& apt-get update && apt-get install -y ${buildDeps} \ 
chrpath libssl-dev libxft-dev libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev \
&& rm -rf /var/lib/apt/lists/* \
&& export OS_ARCH=$(uname -m) \
&& wget https://github.com/mjysci/phantomjs/releases/download/v2.1.1/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz -O /tmp/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz \
&& tar -xzvf /tmp/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz -C /usr/local/bin \
&& rm /tmp/phantomjs-2.1.1-linux_${OS_ARCH}.tar.gz \
&& pip install -r requirements.txt && pip cache purge \
&& apt-get purge -y --auto-remove $buildDeps

EXPOSE $PORT

RUN chmod +x run.sh
CMD ./run.sh $PORT $USERNAME $PASSWORD
