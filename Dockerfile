FROM python:3.8

WORKDIR /mz_bot/ai

COPY . .

RUN apt-get install libpcre3 libpcre3-dev

RUN chmod 777 ./data/swig-3.0.12
RUN ./data/swig-3.0.12/configure && make && make install

RUN swig -version
RUN python3.8 -m pip install -r requirements.txt
RUN pip install uvicorn