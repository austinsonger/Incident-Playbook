FROM python:3.8

WORKDIR /dfirtrack
COPY . /dfirtrack
RUN apt-get update && apt-get -y install postgresql-client nano nginx
RUN pip install -r requirements.txt

RUN mkdocs new markdown
RUN mkdir -p markdown/docs/systems
COPY docker/mkdocs.yml markdown/mkdocs.yml

RUN rm /etc/nginx/sites-enabled/default
COPY docker/nginx.site.conf /etc/nginx/sites-available/dfirtrack
COPY docker/nginx.site.insecure.conf /etc/nginx/sites-available/dfirtrack_insecure
RUN mkdir /etc/nginx/ssl

WORKDIR /dfirtrack
ARG openssl_o
ARG fqdn
ARG openssl_ou
RUN openssl req -newkey rsa:4096 -days 365 -nodes -x509 -subj "/O=$openssl_o/CN=$fqdn/OU=$openssl_ou" -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt
RUN sed -i "s/server_name dfirtrack_app;/server_name $fqdn;/" /etc/nginx/sites-available/dfirtrack
RUN sed -i "s/server_name dfirtrack_app;/server_name $fqdn;/" /etc/nginx/sites-available/dfirtrack_insecure

ARG pgpass_pw
ARG pgpass_user
COPY docker/local_settings.py dfirtrack/local_settings.py
RUN sed -i "s/{{ fqdn }}/$fqdn/" dfirtrack/local_settings.py
RUN sed -i "s/{{ postgresql_user }}/$pgpass_user/" dfirtrack/local_settings.py
RUN sed -i "s/{{ postgresql_user_password }}/$pgpass_pw/" dfirtrack/local_settings.py

ARG disable_https
COPY docker/entrypoint.sh docker/entrypoint.sh
RUN sed -i "s/{{ postgresql_user_password }}/$pgpass_pw/" docker/entrypoint.sh
RUN sed -i "s/{{ disable_https }}/$disable_https/" docker/entrypoint.sh

ARG django_secret_key
RUN sed -i "s/SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGEME')/SECRET_KEY = os.getenv('SECRET_KEY', '$django_secret_key')/" dfirtrack/settings.py

RUN ./manage.py collectstatic
EXPOSE 80
EXPOSE 443
ENTRYPOINT docker/entrypoint.sh