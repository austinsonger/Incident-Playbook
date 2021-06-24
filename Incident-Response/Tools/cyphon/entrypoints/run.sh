#!/bin/sh

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

# wait for PostgreSQL server to start
sleep 10

cd /usr/src/app/cyphon

# migrate db, so we have the latest db schema
su-exec cyphon python manage.py migrate --verbosity 0

# collect static files
su-exec cyphon python manage.py collectstatic --noinput --verbosity 0

# create superuser
if [ "$CYPHON_SUPERUSER" = 'YES' ]; then
    echo "from django.contrib.auth import get_user_model; \
          USER_MODEL = get_user_model(); \
          args = ['$CYPHON_USERNAME', '$CYPHON_PASSWORD']; \
          USER_MODEL.objects.create_superuser(*args)" \
          | python manage.py shell
fi

# load example fixtures
if [ "$LOAD_EXAMPLE_FIXTURES" = 'YES' ]; then
    echo "Loading example fixtures..."
    su-exec cyphon python manage.py loaddata fixtures/starter-fixtures.json
fi

if [ "$CYPHON_ENV" = 'PROD' ]; then
    echo "Running Production Server"
    exec gunicorn cyphon.wsgi:application \
         --name cyphon_django \
         --bind 0.0.0.0:8000 \
         --workers 3 \
         --log-level=warning \
         --log-file=- \
         "$@"  # allow additional arguments when starting container

elif [ "$CYPHON_ENV" = 'TEST' ]; then
    echo "Running Unit Tests"
    exec python manage.py test --noinput "$@"

else
    echo "Running Development Server"
    exec python manage.py runserver 0.0.0.0:8000 "$@"

fi
