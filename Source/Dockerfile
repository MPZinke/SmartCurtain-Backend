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

COPY ./  /usr/local/bin/SmartCurtain/Backend/

RUN python3 -m pip install -r /usr/local/bin/SmartCurtain/Backend/Requirements.txt


# ————————————————————————————————————————————————————— RUNTIME ————————————————————————————————————————————————————— #

ARG NETWORKLOOKUP_BEARERTOKEN
ARG NETWORKLOOKUP_HOST
ARG SMARTCURTAIN_NETWORKNAME

ARG SMARTCURTAIN_BACKEND_API_KEY
ARG SMARTCURTAIN_DB_USER
ARG SMARTCURTAIN_DB_HOST
ARG SMARTCURTAIN_DB_PASSWORD

ENV NETWORKLOOKUP_BEARERTOKEN ${NETWORKLOOKUP_BEARERTOKEN}
ENV NETWORKLOOKUP_HOST ${NETWORKLOOKUP_HOST}
ENV SMARTCURTAIN_NETWORKNAME ${SMARTCURTAIN_NETWORKNAME}

ENV SMARTCURTAIN_BACKEND_API_KEY ${SMARTCURTAIN_BACKEND_API_KEY}
ENV SMARTCURTAIN_DB_USER ${SMARTCURTAIN_DB_USER}
ENV SMARTCURTAIN_DB_HOST ${SMARTCURTAIN_DB_HOST}
ENV SMARTCURTAIN_DB_PASSWORD ${SMARTCURTAIN_DB_PASSWORD}

EXPOSE 8080

CMD ["python3", "/usr/local/bin/SmartCurtain/Backend/Backend.py"]
