FROM python:3.11

# —————————————————————————————————————————————————————— UBUNTU —————————————————————————————————————————————————————— #

# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8
# ENV TZ="America/Chicago"


# ——————————————————————————————————————————————— BACKEND INSTALLATION ——————————————————————————————————————————————— #

ENV TZ="America/Chicago"


COPY ./  /usr/local/bin/SmartCurtain/Backend/
RUN chmod -R 777 /usr/local/bin/SmartCurtain

RUN pip3 install -r /usr/local/bin/SmartCurtain/Backend/Requirements.txt


# ————————————————————————————————————————————————————— RUNTIME ————————————————————————————————————————————————————— #

EXPOSE 8001

ENTRYPOINT ["python3", "/usr/local/bin/SmartCurtain/Backend/Backend.py"]
