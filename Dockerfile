FROM python:3.8.0-alpine


# set work directory
WORKDIR /usr/src/app

# install git
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

# Clone repository
RUN git clone https://github.com/rduk/projectewalleyt /usr/src/app

# copy project
COPY . /usr/src/app/

RUN pip install -r requirements.txt

# expose port
EXPOSE 5000

# init database
RUN python3 /usr/src/app/manage.py db init
RUN python3 /usr/src/app/manage.py db migrate
RUN python3 /usr/src/app/manage.py db upgrade

# test
RUN python3 manage.py test

# generate some data
RUN python3 /usr/src/app/manage.py set_employee
RUN python3 /usr/src/app/manage.py set_users

CMD python3 /usr/src/app/manage.py run
