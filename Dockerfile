FROM python:3.7

RUN python -m pip install --upgrade pip
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code/