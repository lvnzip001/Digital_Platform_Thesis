FROM python:3.9-alpine
LABEL maintainer="lvnzip001@myuct.ac.za"
ENV PYTHONUNBUFFERED 1
RUN mkdir /
WORKDIR /app
COPY ./requirements.txt /app/

COPY ./app /app




CMD [ "python","manage.py","runserver","0.0.0.0:8000"]


RUN apk update \
    &&  apk add --upgrade --no-cache \
        bash openssh curl ca-certificates openssl less htop \
		g++ make wget rsync \
        build-base libpng-dev freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev \
		libgcc libquadmath musl  \
		libgfortran \
		lapack-dev \
	&&  pip install --upgrade pip \
	&&  pip install setuptools \
	&&	apk add --virtual build-deps gcc python3-dev musl-dev \
	&&  apk add freetype-dev \
	&&	pip install -r requirements.txt \
	&&  apk del build-deps 