FROM ubuntu:20.04

# —————————————————————————————————————————————————————— UBUNTU —————————————————————————————————————————————————————— #

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y install locales
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ="America/Chicago"


# —————————————————————————————————————————————— FRONTEND  INSTALLATION —————————————————————————————————————————————— #

RUN apt-get -y install npm curl
# https://stackoverflow.com/a/67491580
RUN npm install npm@latest -g && \
    npm install n -g && \
    n latest

COPY ./ /usr/local/bin/SmartCurtain/Frontend/
RUN rm /usr/local/bin/SmartCurtain/Frontend/package-lock.json
RUN rm -rf /usr/local/bin/SmartCurtain/Frontend/node_modules

RUN npm install --prefix /usr/local/bin/SmartCurtain/Frontend/


# ————————————————————————————————————————————————————— RUNTIME ————————————————————————————————————————————————————— #

ARG SMARTCURTAIN_API_TOKEN

ENV SMARTCURTAIN_API_TOKEN ${SMARTCURTAIN_API_TOKEN}

EXPOSE 3000

CMD ["npm", "start", "--prefix", "/usr/local/bin/SmartCurtain/Frontend/"]
