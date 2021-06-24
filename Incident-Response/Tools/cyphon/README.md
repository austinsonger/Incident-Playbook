[![Build Status](https://travis-ci.org/dunbarcyber/cyphon.svg?branch=master)](https://travis-ci.org/dunbarcyber/cyphon) [![Coverage Status](https://coveralls.io/repos/github/dunbarcyber/cyphon/badge.svg?maxAge=0)](https://coveralls.io/github/dunbarcyber/cyphon) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/c77cf13e942d465389978df70278c2ad)](https://www.codacy.com/app/lhadjchikh/cyphon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dunbarcyber/cyphon&amp;utm_campaign=Badge_Grade) [![Updates](https://pyup.io/repos/github/dunbarcyber/cyphon/shield.svg)](https://pyup.io/repos/github/dunbarcyber/cyphon/) [![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](https://cyphon.readthedocs.io/en/latest/) [![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/cyphonproject/Lobby)

[![Cyphon](https://github.com/dunbarcyber/cyphon/blob/master/docs/source/_static/images/cyphon-logo.png)](https://cyphon.io)

# Cyphon

# NOTE: This project is no longer actively maintained.

## Collect, Alert, Respond

Cyphon is an incident-response platform that receives, processes, and triages events to create a more efficient analytic workflow — aggregating data, bundling and prioritizing alerts, and empowering analysts to investigate and document incidents.

**Collect**

Cyphon collects data from a variety of sources, including emails, log messages, and social media. It lets you shape the data however you like, so it’s easier for you to analyze. You can also enhance your data with automated analyses, like geocoding.

![Cyphon admin dashboard](https://github.com/dunbarcyber/cyphon/blob/master/docs/source/_static/images/screenshots/cyphon-admin.png)

**Alert**

Cyphon creates alerts for important data as it arrives, so you’re notified when something of interest happens. You can prioritize alerts using custom rulesets, and bundle related alerts so you don't get inundated.

![Cyclops UI dashboard view](https://github.com/dunbarcyber/cyphon/blob/master/docs/source/_static/images/screenshots/cyclops-dashboard.png)

**Respond**

Analysts can quickly investigate alerts by exploring related data, and annotate alerts with their findings. With JIRA integration, they can escalate important alerts by creating a ticket in Service Desk.

![Cyclops UI alert view](https://github.com/dunbarcyber/cyphon/blob/master/docs/source/_static/images/screenshots/cyclops-alerts.png)

![Cyclops UI related data panel](https://github.com/dunbarcyber/cyphon/blob/master/docs/source/_static/images/screenshots/related-data.png)

## Use Cases

### Incident Management

Many organizations manage post-processed security events as email notifications, which is incredibly inefficient. An inbox flooded with alert notifications creates an environment where critical issues are overlooked and rarely investigated.

Cyphon eliminates this issue by throttling events and prioritizing them based on user-defined rules. Analysts can quickly investigate incidents by correlating other data sets against indicators that matter. They can then annonate alerts with the results of their analysis. 

Today, Cyphon supports integrations with Bro, Snort, Nessus, and other popular security products.

### Social Media Monitoring

Leveraging publicly available APIs, Cyphon can collect data from streaming sources. Search is based on keywords, geofencing, and adhoc parameters. Cyphon supports the current version of the [Twitter Public Streams API](https://dev.twitter.com/streaming/public).

### IoT and Sensor Data Processing

Cyphon can process events from any sensor type, offering a unique way to analyze information from physical environments.  


## Features

* Aggregate data from numerous sources: email, logs, social media, and APIs
* Enhance data with automated analyses, like geoip
* Generate custom alerts with push notifications
* Throttle alerts and bundle related incidents
* View alerts by category, priority, and source
* Investigate alerts and track work performed


## Architecture

The Cyphon platform is made up of a backend data processing engine ("Cyphon Engine") and a security operations front end UI for visualization ("Cyclops"). They are maintained in separate projects. The Cyclops project can be found [here](https://github.com/dunbarcyber/cyclops).


## Deployment

Cyphon works with the help of several open source projects. To get Cyphon up and running, you'll need to install all of its dependencies. We've simplified this process by using [Docker](https://www.docker.com/), which allows you to easily deploy an application as a set of microservices. Additionally, we've created a set of files for running Cyphon in both development and production environments. Employing a Docker Compose file enables you to quickly install and run Cyphon and the other services it uses, including:

* [PostgreSQL](https://www.postgresql.org/) relational database
* [RabbitMQ](https://www.rabbitmq.com/) message broker
* [Logstash](https://www.elastic.co/products/logstash/) data ingestion tool

Our Docker Compose files are available on GitHub as [Cyphondock](https://github.com/dunbarcyber/cyphondock). If you'd like to work with our Docker image directly, you can find it on [Docker Hub](https://hub.docker.com/r/dunbar/cyphon/):


## Documentation

Consult our [official documentation](http://cyphon.readthedocs.io/en/latest/index.html) to learn more about Cyphon. The docs include set-up instructions and a description of Cyphon’s API. Documentation for Cyclops can be found [here](http://cyphon-ui.readthedocs.io/en/latest/index.html).


## License

Cyphon is free software and available for personal or professional use. The Cyphon Project is maintained by [ControlScan](https://www.controlscan.com/security/managed-detection-response-mdr/) and is distributed under a dual license. The Cyphon Engine is distributed under the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html). Cyclops is subject to a non-commercial use license.
