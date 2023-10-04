FROM python:3.11

# ——————————————————————————————————————————————— BACKEND INSTALLATION ——————————————————————————————————————————————— #

ENV TZ="America/Chicago"


COPY ./  /usr/local/bin/SmartCurtain/Backend/
RUN chmod -R 777 /usr/local/bin/SmartCurtain

RUN pip3 install -r /usr/local/bin/SmartCurtain/Backend/Requirements.txt


# ————————————————————————————————————————————————————— RUNTIME ————————————————————————————————————————————————————— #

EXPOSE 8001

ENTRYPOINT ["python3", "/usr/local/bin/SmartCurtain/Backend/Backend.py"]
