FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PATH /usr/local/bin:$PATH

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install pipenv
RUN pipenv run pip install --upgrade pip==18.0
RUN pipenv install
RUN pipenv install --dev

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["pipenv", "run"]
CMD ["runserver"]
