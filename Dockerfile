#base image
FROM python:3.7.2-alpine

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt

# add app
COPY . /usr/src/app

# run server
CMD python3 app.py 