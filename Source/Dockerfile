FROM python:3.11

# ——————————————————————————————————————————————— BACKEND INSTALLATION ——————————————————————————————————————————————— #

ENV TZ="America/Chicago"


COPY ./  /usr/local/bin/SmartCurtain/Backend/
RUN chmod -R 777 /usr/local/bin/SmartCurtain

RUN pip3 install .


# ————————————————————————————————————————————————————— RUNTIME ————————————————————————————————————————————————————— #

EXPOSE 8001

ENTRYPOINT ["python3", "/usr/local/bin/SmartCurtain/Backend/Backend.py"]
