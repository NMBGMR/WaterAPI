#
FROM python:3.9


RUN apt-get update
RUN #apt-get install libsqlite3-mod-spatialite -y
RUN apt-get install unixodbc-dev -y
RUN apt-get install freetds-dev -y
COPY ./requirements.txt /api/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

#
COPY . /api/