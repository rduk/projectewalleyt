
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "app.py" ]

# pull official base image
FROM python:3.8.0-alpine


# set work directory
WORKDIR /usr/src/app

# install git
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh

# Clone repository
RUN git clone https://github.com/rduk/projectewalleyt /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r .requirements.txt

# expose port
EXPOSE 8080

# copy project
COPY . /usr/src/app/

# init database
RUN python main/manage.py db init
RUN python main/manage.py db migrate
RUN python main/manage.py db upgrade

# test
RUN python main/manage.py test

