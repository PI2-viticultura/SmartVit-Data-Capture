FROM python:3.7.1-stretch

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    curl https://bootstrap.pypa.io/get-pip.py | python && \ 
    pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip3 install -r requirements.txt

COPY . /app/

CMD ["python3", "app.py", "run"]