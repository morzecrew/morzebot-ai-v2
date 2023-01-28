FROM python:3.9

WORKDIR /mz_bot/ai

COPY . .

RUN tar -xvf ./data/swig-3.0.12.tar -C ./data

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LC_ALL C

RUN locale

RUN apt-get install libpcre3 libpcre3-dev

RUN chmod 777 ./data/swig-3.0.12
RUN ./data/swig-3.0.12/configure && make && make install

RUN swig -version
RUN python3.9 -m pip install -r requirements.txt

RUN python3.9 .lib/trainer.py