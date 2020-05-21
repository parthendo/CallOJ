# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6

# Running Java inside the Python container using a concept of multistage build
# Documentation: https://docs.docker.com/develop/develop-images/multistage-build/

RUN mkdir /usr/lib/jvm
RUN mkdir /usr/lib/jvm/java-8-openjdk-amd64
COPY --from=openjdk:8 /usr/local/openjdk-8 /usr/lib/jvm/java-8-openjdk-amd64
# RUN ["/bin/bash", "-c", "ls -l /usr/lib/jvm/java-8-openjdk-amd64/bin"]

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /CallOJ

WORKDIR /CallOJ

ADD . /CallOJ/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["/bin/bash", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]

