FROM ubuntu:14.04

MAINTAINER Dockerfiles

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && apt-get install -y \
	git 

# install uwsgi now because it takes a little while

COPY . /home/git/sparta-project/


# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
RUN bash /home/git/sparta-project/install.sh

EXPOSE 80
#CMD ["supervisord", "-n"]