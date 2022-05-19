FROM python:3.7.3-alpine3.9 as prod

# RUN mkdir /app/
# WORKDIR /app/

COPY iot-and-big-data-analytics-project-2022_08_team ./
COPY iot-and-big-data-analytics-project-2022_08_team/requirements.txt ./
RUN pip install -r requirements.txt

COPY  /app/

EXPOSE 8000

CMD ["python", "main.py"]