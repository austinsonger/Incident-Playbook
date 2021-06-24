############################################################
# Dockerfile to run a Django-based web application
# Based on a Python 3.6 image
#
# Copyright 2017-2019 ControlScan, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
#
############################################################

FROM python:3.6-alpine

MAINTAINER Cyphon <cyphondev@controlscan.com>

ARG UID=1000
ARG GID=1000

ENV CYPHON_HOME /usr/src/app
ENV LOG_DIR     /var/log/cyphon
ENV PATH        $PATH:$CYPHON_HOME
ENV NLTK_DATA   /usr/share/nltk_data

# copy requirements.txt to the image
COPY requirements.txt $CYPHON_HOME/requirements.txt

# install Alpine and Python dependencies
RUN apk add -U --no-cache \
      --repository http://dl-5.alpinelinux.org/alpine/edge/main/ \
      --repository http://dl-5.alpinelinux.org/alpine/edge/testing/ \
      --repository http://dl-5.alpinelinux.org/alpine/edge/community/ \
      binutils \
      gdal \
      postgis \
      proj-dev \
      py3-gdal \
      su-exec \
&& ln -s /usr/lib/libgdal.so.20 /usr/lib/libgdal.so \
&& ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so \
&& apk add -U --no-cache \
      --repository http://dl-5.alpinelinux.org/alpine/edge/main/ \
      --repository http://dl-5.alpinelinux.org/alpine/edge/testing/ \
      --repository http://dl-5.alpinelinux.org/alpine/edge/community/ \      
      -t build-deps \
      build-base \
      libffi-dev \
      libressl-dev \
      openssl-dev \
      linux-headers \
      musl-dev \
      postgis \
      postgresql-dev \
      python3-dev \
      jpeg-dev \
      zlib-dev \
      tiff-dev \
&& pip install --upgrade pip \
&& pip install -r $CYPHON_HOME/requirements.txt \
&& apk del build-deps \
&& python -m nltk.downloader -d /usr/local/share/nltk_data punkt wordnet 

# create unprivileged user
RUN addgroup -S -g $GID cyphon && adduser -S -G cyphon -u $UID cyphon

# create application subdirectories
RUN mkdir -p $CYPHON_HOME \
             $CYPHON_HOME/media \
             $CYPHON_HOME/static \
             $LOG_DIR

# copy project to the image
COPY cyphon $CYPHON_HOME/cyphon

# copy entrypoint scripts to the image
COPY entrypoints $CYPHON_HOME/entrypoints

COPY cyphon/cyphon/settings/base.example.py $CYPHON_HOME/cyphon/cyphon/settings/base.py
COPY cyphon/cyphon/settings/conf.example.py $CYPHON_HOME/cyphon/cyphon/settings/conf.py
COPY cyphon/cyphon/settings/dev.example.py $CYPHON_HOME/cyphon/cyphon/settings/dev.py
COPY cyphon/cyphon/settings/prod.example.py $CYPHON_HOME/cyphon/cyphon/settings/prod.py

# set owner:group and permissions
RUN chown -R cyphon:cyphon $CYPHON_HOME \
 && chmod -R 775 $CYPHON_HOME \
 && chown -R cyphon:cyphon $LOG_DIR \
 && chmod -R 775 $LOG_DIR

WORKDIR $CYPHON_HOME/cyphon

VOLUME ["$CYPHON_HOME/keys", "$CYPHON_HOME/media", "$CYPHON_HOME/static"]

EXPOSE 8000

CMD $CYPHON_HOME/entrypoints/run.sh
