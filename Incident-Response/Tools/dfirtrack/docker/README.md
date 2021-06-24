# How to run the DFIRTrack Docker Container

To run dfirtrack in a docker container simply execute `docker-compose up` in this directory. **Before doing so, please check the .env file that is located in the same directory and make necessary changes.** This file is used to set internal variables, e.g. passwords and usernames. Make sure to rebuild the container (e.g. with `docker-compose up --build`) whenever there are changes in the .env file.

The container uses the local version of dfirtrack. It uses gunicorn and nginx to serve the application and a separate container for the postgres database. The database is using a docker volume to persist changes - when you want to start with a fresh database, simply delete the volume. Due to this design, the docker container can be used for development as well as for production purposes.

To use the container in a cloud environment, most of the settings can also be changed with environment variables. The following list shows the available environment variables.

```
DB_NAME: dfirtrack               # name of the database
DB_USER: test                    # username of the database
DB_PASSWORD: secret              # password of the database
DB_HOST: db                      # hostname of the database
DB_PORT: 5432                    # port of the database
FQDN: dfirtrack.test             # fqdn for dfirtrack
DISABLE_HTTPS: 'true'            # 'true' to disable HTTPS
SECRET_KEY: sup3r_s3cr3t_k3y     # django secret key
```

Note: The build process of the container creates the SSL certificate with the FQDN in the `.env` file. When you change the FQDN in the environment variables, SSL requests won't work. You should only change the `FQDN` parameter, if you also want to set `DISABLE_HTTPS` to `'true'`. In production environments, the `DISABLE_HTTPS` setting should only be used behind a load balancer or another proxy which enables encryption.
