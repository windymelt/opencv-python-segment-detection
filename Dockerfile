FROM jjanzic/docker-python3-opencv:latest
RUN mkdir /app
WORKDIR /app

RUN pip install opencv-contrib-python

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev libimlib2 libimlib2-dev

# soccr
RUN mkdir /tmpwork
WORKDIR /tmpwork
RUN wget -O ssocr.tar.gz https://github.com/auerswal/ssocr/archive/refs/tags/v2.21.0.tar.gz
RUN tar zxvf ssocr.tar.gz
WORKDIR ssocr-2.21.0
RUN ls
RUN make && make install
WORKDIR /app
RUN rm -rf /tmpwork