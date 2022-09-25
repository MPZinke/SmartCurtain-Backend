FROM ubuntu:20.04

# —————————————————————————————————————————————————————— UBUNTU —————————————————————————————————————————————————————— #

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y install locales
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ="America/Chicago"


# ——————————————————————————————————————————————— BACKEND INSTALLATION ——————————————————————————————————————————————— #

RUN apt-get -y install libpq-dev
RUN apt-get -y install python3.10
RUN apt-get -y install python3-pip

COPY Backend/  /usr/local/bin/SmartCurtain/Backend/

RUN python3 -m pip install -r /usr/local/bin/SmartCurtain/Backend/Requirements.txt

# —————————————————————————————————————————————— FRONTEND  INSTALLATION —————————————————————————————————————————————— #

RUN apt-get -y install npm curl
# https://stackoverflow.com/a/67491580
RUN npm install npm@latest -g && \
    npm install n -g && \
    n latest

COPY Frontend/ /usr/local/bin/SmartCurtain/Frontend/
RUN rm /usr/local/bin/SmartCurtain/Frontend/package-lock.json
RUN rm -rf /usr/local/bin/SmartCurtain/Frontend/node_modules

RUN npm install --prefix /usr/local/bin/SmartCurtain/Frontend/


# ————————————————————————————————————————————————————— RUNTIME ————————————————————————————————————————————————————— #

COPY Run.sh /usr/local/bin/SmartCurtain/


ARG NETWORKLOOKUP_BEARERTOKEN
ARG NETWORKLOOKUP_HOST
ARG SMARTCURTAIN_NETWORKNAME
ARG SMARTCURTAIN_DB_USER
ARG SMARTCURTAIN_DB_HOST
ARG SMARTCURTAIN_API_TOKEN

ENV NETWORKLOOKUP_BEARERTOKEN ${NETWORKLOOKUP_BEARERTOKEN}
ENV NETWORKLOOKUP_HOST ${NETWORKLOOKUP_HOST}
ENV SMARTCURTAIN_NETWORKNAME ${SMARTCURTAIN_NETWORKNAME}
ENV SMARTCURTAIN_DB_USER ${SMARTCURTAIN_DB_USER}
ENV SMARTCURTAIN_DB_HOST ${SMARTCURTAIN_DB_HOST}
ENV SMARTCURTAIN_API_TOKEN ${SMARTCURTAIN_API_TOKEN}

EXPOSE 3000
EXPOSE 8080

CMD bash "/usr/local/bin/SmartCurtain/Run.sh"
