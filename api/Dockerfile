#
FROM python:3.9

#
WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install unixodbc-dev -y
RUN apt-get install freetds-dev -y

#
COPY ./requirements.txt .

#
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
COPY . .