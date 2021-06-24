# Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/). This project adheres to [Semantic Versioning](http://semver.org/).

<a name="1.6.6"></a>
## [1.6.6](https://github.com/dunbarcyber/cyphon/compare/1.6.5...1.6.6) (2018-06-14)

### Changed

- **alerts.models** + **cyphon.settings.conf**: added conditional setting ALERTS.DISABLE_COLLECTION_SEARCH to determine if alert should search backend storage for missing alert data. ([09c246b](https://github.com/dunbarcyber/cyphon/commit/09c246b))

<a name="1.6.5"></a>
## [1.6.5](https://github.com/dunbarcyber/cyphon/compare/1.6.4...1.6.5) (2018-06-11)

### Fixed

- **Dockerfile**: changed apk packages to download libressl instead of openssl due to multiple packages upgrading from open to libre. ([75172dc](https://github.com/dunbarcyber/cyphon/commit/75172dc))

### Changed

- **requirements.txt**: removed cryptography from dependencies due to it depending on openssl and since it is not used in the project anymore. ([f707446](https://github.com/dunbarcyber/cyphon/commit/f707446))

<a name="1.6.4"></a>
## [1.6.4](https://github.com/dunbarcyber/cyphon/compare/1.6.3...1.6.4) (2018-04-03)

### Added

- **cyphon.settings.conf**: added CYCLOPS.API_TIMEOUT to settings file ([249c0ef](https://github.com/dunbarcyber/cyphon/commit/249c0ef))

### Fixed

- **setup.py**: fixed failing CI build due to pip 10 update moving all it's internal API to `._internal` ([92417d1](https://github.com/dunbarcyber/cyphon/commit/92417d1))

<a name="1.6.3"></a>
## [1.6.3](https://github.com/dunbarcyber/cyphon/compare/1.6.2...1.6.3) (2018-03-30)

### Added

- **cyphon.settings.conf**: added `APPUSERS.ONLY_SHOW_STAFF` to settings file [PR #482](https://github.com/dunbarcyber/cyphon/pull/482) ([055de63](https://github.com/dunbarcyber/cyphon/commit/055de63))

<a name="1.6.2"></a>
## [1.6.2](https://github.com/dunbarcyber/cyphon/compare/1.6.1...1.6.2) (2018-03-22)

### Added

- **ambassador.transport**: added `Transport.ensure_cargo()` method ([a73e0b8](https://github.com/dunbarcyber/cyphon/commit/a73e0b8))

### Fixed

- **aggregator.pumproom.streamcontroller**: prevented exceptions from locking Streams [PR #457](https://github.com/dunbarcyber/cyphon/pull/457) ([0e88556](https://github.com/dunbarcyber/cyphon/commit/0e88556))
- **sifter.condensers.tests.pages**: fixed broken functional tests for offscreen elements [PR #433](https://github.com/dunbarcyber/cyphon/pull/433) ([e2cd38b](https://github.com/dunbarcyber/cyphon/commit/e2cd38b))
- **target.locations**: removed mixin from `LocationManager` to fix mocking for Sphinx [PR #396](https://github.com/dunbarcyber/cyphon/pull/396) ([b441361](https://github.com/dunbarcyber/cyphon/commit/b441361))
- **tox.ini**: added missing Twitter environment variables for tests ([c0092f7](https://github.com/dunbarcyber/cyphon/commit/c0092f7))

<a name="1.6.1"></a>
## [1.6.1](https://github.com/dunbarcyber/cyphon/compare/1.6.0...1.6.1) (2018-02-06)

### Added

- **utils.dbutils**: added `SQCount` subquery class [PR #364](https://github.com/dunbarcyber/cyphon/pull/364) ([91d1829](https://github.com/dunbarcyber/cyphon/commit/91d1829))

### Changed

- **cyclops.conf**: updated Cyclops version to 0.5.4 [PR #361](https://github.com/dunbarcyber/cyphon/pull/361) ([6536c91](https://github.com/dunbarcyber/cyphon/commit/6536c91))
- **utils.dbutils**: optimized `count_by_group()` [PR #364](https://github.com/dunbarcyber/cyphon/pull/364) ([91d1829](https://github.com/dunbarcyber/cyphon/commit/91d1829))

### Fixed

- **alerts.views**: optimized `AlertViewSet.counts_by_collection()` to prevent timeouts [PR #364](https://github.com/dunbarcyber/cyphon/pull/364) ([91d1829](https://github.com/dunbarcyber/cyphon/commit/91d1829))
- **sieves.models**: catch exception raised by a numeric comparison of a null value [PR #376](https://github.com/dunbarcyber/cyphon/pull/376) ([8352bb2](https://github.com/dunbarcyber/cyphon/commit/8352bb2))

### Removed

- **alerts**: removed `AlertManager.api_queryset()` [PR #377](https://github.com/dunbarcyber/cyphon/pull/377) ([644c270](https://github.com/dunbarcyber/cyphon/commit/644c270))
- **tox.ini**: removed py27-docs from tests [PR #383](https://github.com/dunbarcyber/cyphon/pull/383) ([2d73123](https://github.com/dunbarcyber/cyphon/commit/2d73123))


<a name="1.6.0"></a>
## [1.6.0](https://github.com/dunbarcyber/cyphon/compare/1.5.3...1.6.0) (2018-01-11)

### Added

- **distilleries**: added `name` property to Distillery model [PR #320](https://github.com/dunbarcyber/cyphon/pull/320) ([d25c147](https://github.com/dunbarcyber/cyphon/commit/d25c147))
- **query.search**: added before and after filters to search views ([c3f3e64](https://github.com/dunbarcyber/cyphon/commit/c3f3e64))
- **query.search**: added time filtering to alert results ([a993356](https://github.com/dunbarcyber/cyphon/commit/a993356))

### Changed

- **contexts**: changed `ContextManager.get_by_natural_key()` and `ContextFilterManager.get_by_natural_key()` to use `Distillery.name` [PR #320](https://github.com/dunbarcyber/cyphon/pull/320) ([d25c147](https://github.com/dunbarcyber/cyphon/commit/d25c147))
- **cyclops.conf**: updated Cyclops version to 0.5.2 ([cc48152](https://github.com/dunbarcyber/cyphon/commit/cc48152))
- **cyphon.tasks**: Monitor status is updated through polling ([0eff575](https://github.com/dunbarcyber/cyphon/commit/0eff575))
- **distilleries**: changed `DistilleryManager.get_by_natural_key()` to use `Distillery.name` [PR #320](https://github.com/dunbarcyber/cyphon/pull/320) ([d25c147](https://github.com/dunbarcyber/cyphon/commit/d25c147))
- **monitors**: Monitor status is updated through polling ([0eff575](https://github.com/dunbarcyber/cyphon/commit/0eff575))
- **query.search**: search terms joined with AND instead of OR ([09659ee](https://github.com/dunbarcyber/cyphon/commit/09659ee))
- **query.search**: added alert field filtering [PR #338](https://github.com/dunbarcyber/cyphon/pull/338) ([a91498e](https://github.com/dunbarcyber/cyphon/commit/a91498e))
- **query.search.distillery_filter_parameter**: filters by given distillery name instead of the combination warehouse.collection. ([5fbb1a8](https://github.com/dunbarcyber/cyphon/commit/5fbb1a8))

### Fixed

- **docs**: fixed incorrect token request URL in JIRA oauth example [PR #315](https://github.com/dunbarcyber/cyphon/pull/315) ([7008c64](https://github.com/dunbarcyber/cyphon/commit/7008c64))
- **query.search**: fixed search parameter for Distillery name with hyphens ([d64e38d](https://github.com/dunbarcyber/cyphon/commit/d64e38d))
- **query.search**: fixed IPAddress field searches ([44feca7](https://github.com/dunbarcyber/cyphon/commit/44feca7))
- **sifter.mailsifter**: allow either valid content type or valid file extension for email attachments [PR #319](https://github.com/dunbarcyber/cyphon/pull/319) ([efef0bc](https://github.com/dunbarcyber/cyphon/commit/efef0bc))
- **warehouses**: added lowercase_validator to `Warehouse.name` for Elasticsearch compatibility ([598dd96](https://github.com/dunbarcyber/cyphon/commit/598dd96))
- **utils.geometry.shapes**: fixed handling of hash-based Geo-point datatypes [PR #273](https://github.com/dunbarcyber/cyphon/pull/273) ([38b6e49](https://github.com/dunbarcyber/cyphon/commit/38b6e49))
- **utils.geometry.shapes**: catch all exceptions in `convert_to_point()` [PR #298](https://github.com/dunbarcyber/cyphon/pull/298) ([598dd96](https://github.com/dunbarcyber/cyphon/commit/598dd96))

### Removed

- **reciever**: removed Monitor queue consumer ([0eff575](https://github.com/dunbarcyber/cyphon/commit/0eff575))


<a name="1.5.3"></a>
## [1.5.3](https://github.com/dunbarcyber/cyphon/compare/1.5.2...1.5.3) (2017-10-13)

### Fixed

- **Dockerfile**: cached NLTK data in the Docker image [PR #247](https://github.com/dunbarcyber/cyphon/pull/247) ([9b4cf31](https://github.com/dunbarcyber/cyphon/commit/9b4cf31))
- **monitors**: fixed bug in `Monitor._get_inactive_seconds()` for new Monitors [PR #256](https://github.com/dunbarcyber/cyphon/pull/256) ([1e154a9](https://github.com/dunbarcyber/cyphon/commit/1e154a9))


<a name="1.5.2"></a>
## [1.5.2](https://github.com/dunbarcyber/cyphon/compare/1.5.1...1.5.2) (2017-10-03)

### Fixed

- **aggregator.streams**: prevented timeouts on Stream object admin pages [PR #245](https://github.com/dunbarcyber/cyphon/pull/245) ([6baa7ed](https://github.com/dunbarcyber/cyphon/commit/6baa7ed))


<a name="1.5.1"></a>
## [1.5.1](https://github.com/dunbarcyber/cyphon/compare/1.5.0...1.5.1) (2017-10-02)

### Changed

- **utils.validators**: changed `db_name_validator()` to allow hyphens and disallow $ [PR #241](https://github.com/dunbarcyber/cyphon/pull/241) ([8c03a48](https://github.com/dunbarcyber/cyphon/commit/8c03a48))

### Fixed

- **monitors**: fixed time calculations used in `Monitor.update_status()` [PR #242](https://github.com/dunbarcyber/cyphon/pull/242) ([e48c089](https://github.com/dunbarcyber/cyphon/commit/e48c089))


<a name="1.5.0"></a>
## [1.5.0](https://github.com/dunbarcyber/cyphon/compare/1.4.2...1.5.0) (2017-09-26)

### Added

- **alerts**: added ``associated_tags`` property to Alerts ([dd274ca](https://github.com/dunbarcyber/cyphon/commit/dd274ca))
- **alerts**: added ``tag_relations`` property to Alerts and Comments ([ae10cf1](https://github.com/dunbarcyber/cyphon/commit/ae10cf1))
- **alerts**: added ``tags`` field to ``AlertDetailSerializer`` based on ``Alert.associated_tags`` property ([119bf21](https://github.com/dunbarcyber/cyphon/commit/d71474b))
- **articles**: added Article model [PR #196](https://github.com/dunbarcyber/cyphon/pull/196) ([1dcf272](https://github.com/dunbarcyber/cyphon/commit/1dcf272))
- **cyphon.settings**: added Elasticsearch index settings ([66f9bbb](https://github.com/dunbarcyber/cyphon/commit/66f9bbb))
- **cyphon.settings**: added settings for data uploads ([9523dfb](https://github.com/dunbarcyber/cyphon/commit/9523dfb))
- **cyphon.settings**: added localization settings ([a7adde9](https://github.com/dunbarcyber/cyphon/commit/a7adde9))
- **cyphon.urls**: REST API endpoints for Tags ([119bf21](https://github.com/dunbarcyber/cyphon/commit/119bf21))
- **distilleries**: added ``engine`` property to Distilleries ([6e110e4](https://github.com/dunbarcyber/cyphon/commit/6e110e4))
- **docs**: docs for Articles, Tags, Topics, and DataTaggers [PR #225](https://github.com/dunbarcyber/cyphon/pull/225) ([879af9d](https://github.com/dunbarcyber/cyphon/commit/879af9d))
- **engines.elasticsearch**: added ``ElasticsearchEngine.create_template()`` method ([66f9bbb](https://github.com/dunbarcyber/cyphon/commit/66f9bbb))
- **requirements.txt**: django-ckeditor package ([de94ecf](https://github.com/dunbarcyber/cyphon/commit/de94ecf))
- **tags**: TagRelation, Topic, and DataTagger models [PR #178](https://github.com/dunbarcyber/cyphon/pull/178) ([119bf21](https://github.com/dunbarcyber/cyphon/commit/119bf21))
- **tags**: post-save signals for tagging Alerts and Comments ([41e7f87](https://github.com/dunbarcyber/cyphon/commit/41e7f87))
- **warehouses**: post_save signal receiver to create Elasticsearch index templates ([35627bc](https://github.com/dunbarcyber/cyphon/commit/35627bc))
- **utils.validators**: ``lowercase_validator()`` function ([5b0ce6f](https://github.com/dunbarcyber/cyphon/commit/5b0ce6f))

### Changed

- **alerts**: refactored ``Alert.notes`` into new Analysis model [PR #202](https://github.com/dunbarcyber/cyphon/pull/202) ([fa3077b](https://github.com/dunbarcyber/cyphon/commit/fa3077b))
- **alerts**: used ``RichTextUploadingField`` for ``Comment.notes`` ([86c1635](https://github.com/dunbarcyber/cyphon/commit/86c1635))
- **cyphon.settings**: removed local static assets options from CYCLOPS settings ([d62e95f](https://github.com/dunbarcyber/cyphon/commit/d62e95f))
- **cyclops**: removed local static asset options from the view and replaced it with urls ([d62e95f](https://github.com/dunbarcyber/cyphon/commit/d62e95f))
- **docs**: updated configuration docs to reflect the removal of Cyclops static assets ([d62e95f](https://github.com/dunbarcyber/cyphon/commit/d62e95f))
- **docs**: moved fixture docs to user manual ([c9122c0](https://github.com/dunbarcyber/cyphon/commit/c9122c0))
- **docs**: updated instructions for project configuration ([d87111f](https://github.com/dunbarcyber/cyphon/commit/d87111f))
- **responder.actions**: ordered Actions by title ([9298b82](https://github.com/dunbarcyber/cyphon/commit/9298b82))

### Fixed

- **alerts:** prevented duplicate ``muzzle_hash`` when ``Alert.level`` is changed [Issue #223](https://github.com/dunbarcyber/cyphon/issues/223) ([68a1acc](https://github.com/dunbarcyber/cyphon/commit/68a1acc))
- **contexts:** prevented server error if Context query can't be completed [PR #224](https://github.com/dunbarcyber/cyphon/issues/224) ([9209dd6](https://github.com/dunbarcyber/cyphon/commit/9209dd6))
- **engines.elasticsearch**: prevented error from unmatched quote in query string [PR #209](https://github.com/dunbarcyber/cyphon/pull/209) ([ed94ac0](https://github.com/dunbarcyber/cyphon/commit/ed94ac0))
- **engines.elasticsearch**: avoided mapping conflicts in Kibana by creating index templates [PR #213](https://github.com/dunbarcyber/cyphon/pull/213) ([61b111c](https://github.com/dunbarcyber/cyphon/commit/61b111c))
- **sifter.sieves**: prevented endless recursion in Sieves [PR #208](https://github.com/dunbarcyber/cyphon/pull/208) ([5f3fec0](https://github.com/dunbarcyber/cyphon/commit/5f3fec0))

### Removed

- **alerts.models**: removed ``Alert.tags`` field ([119bf21](https://github.com/dunbarcyber/cyphon/commit/119bf21))
- **cyphon.settings**: removed CORS settings ([3dea449](https://github.com/dunbarcyber/cyphon/commit/3dea449))
- **requirements.txt**: removed django-cors-headers ([3dea449](https://github.com/dunbarcyber/cyphon/commit/3dea449))

<a name="1.4.2"></a>
## [1.4.2](https://github.com/dunbarcyber/cyphon/compare/1.4.1...1.4.2) (2017-08-21)

### Changed

- **monitors**: status of Monitors is updated on save [PR #186](https://github.com/dunbarcyber/cyphon/pull/186) ([18a4ab8](https://github.com/dunbarcyber/cyphon/commit/18a4ab8))

### Fixed

- **engines.elasticsearch**: fixed default value for Elasticsearch timeout ([22cd0b5](https://github.com/dunbarcyber/cyphon/commit/22cd0b5))


<a name="1.4.1"></a>
## [1.4.1](https://github.com/dunbarcyber/cyphon/compare/1.4.0...1.4.1) (2017-08-14)

### Fixed

- **monitors**: fixed bug that prevented red monitors from changing back to green [PR #184](https://github.com/dunbarcyber/cyphon/pull/184) ([28f1f64](https://github.com/dunbarcyber/cyphon/commit/28f1f64))


<a name="1.4.0"></a>
## [1.4.0](https://github.com/dunbarcyber/cyphon/compare/1.3.0...1.4.0) (2017-08-14)

### Added

- **alerts**: ``Alert.muzzle_hash`` field [PR #130](https://github.com/dunbarcyber/cyphon/pull/130) ([efaa627](https://github.com/dunbarcyber/cyphon/commit/efaa627))
- **alerts**: email notifications for Alert comments [PR #139](https://github.com/dunbarcyber/cyphon/pull/139) ([bd968c1](https://github.com/dunbarcyber/cyphon/commit/bd968c1))
- **cyphon.choices**: range choices ([1c414aa](https://github.com/dunbarcyber/cyphon/commit/1c414aa))
- **cyphon.version**: added Cyphon version to headers ([40c123f](https://github.com/dunbarcyber/cyphon/commit/40c123f), [08ff612](https://github.com/dunbarcyber/cyphon/commit/08ff612))
- **docs**: search query docs ([bfe06fd](https://github.com/dunbarcyber/cyphon/commit/bfe06fd))
- **docs**: Alert bulk admin docs ([3d963b1](https://github.com/dunbarcyber/cyphon/commit/3d963b1))
- **docs**: secrets management ([7cdddc2](https://github.com/dunbarcyber/cyphon/commit/7cdddc2), [4a110fc](https://github.com/dunbarcyber/cyphon/commit/4a110fc))
- **query.search**: search query classes ([76dac5d](https://github.com/dunbarcyber/cyphon/commit/76dac5d))
- **query.search**: search endpoint [PR #136](https://github.com/dunbarcyber/cyphon/pull/136) ([56bd2ce](https://github.com/dunbarcyber/cyphon/commit/56bd2ce))
- **requirements.txt**: boto3, django-s3-storage, and ec2-metadata packages [PR #134](https://github.com/dunbarcyber/cyphon/pull/134) ([62751ee](https://github.com/dunbarcyber/cyphon/commit/62751ee))
- **sifter.sieves**: numeric rules [PR #129](https://github.com/dunbarcyber/cyphon/pull/129) ([0fba6f4](https://github.com/dunbarcyber/cyphon/commit/0fba6f4))
- **utils.parserutils**: ``merge_dict()`` and ``abridge_dict()`` functions ([44e9fcd](https://github.com/dunbarcyber/cyphon/commit/44e9fcd))
- **utils.settings**: default configuration and pull secrets from SSM ([7796fc9](https://github.com/dunbarcyber/cyphon/commit/7796fc9))

### Changed

- **alerts**: only fields defined in Container are shown in Alert data [PR #127](https://github.com/dunbarcyber/cyphon/pull/127) ([cdd0c68](https://github.com/dunbarcyber/cyphon/commit/cdd0c68))
- **alerts**: doc_id field included in serialized Alert detail [PR #145](https://github.com/dunbarcyber/cyphon/pull/145) ([c62dca4](https://github.com/dunbarcyber/cyphon/commit/c62dca4))
- **cyphon.settings, engines.elasticsearch**: support more Elasticsearch configuration options [PR #170](https://github.com/dunbarcyber/cyphon/pull/170) ([91312dc](https://github.com/dunbarcyber/cyphon/commit/91312dc), [51a2a68](https://github.com/dunbarcyber/cyphon/commit/51a2a68))
- **watchdogs**: removed Alert table locking [PR #130](https://github.com/dunbarcyber/cyphon/pull/130) ([efaa627](https://github.com/dunbarcyber/cyphon/commit/efaa627))

### Fixed

- **cyphon.settings**: corrected ``backupCount`` setting for logging handlers ([e150db1](https://github.com/dunbarcyber/cyphon/commit/e150db1))

### Removed

- **docs**: removed Docker instructions ([87012e2](https://github.com/dunbarcyber/cyphon/commit/87012e2))


<a name="1.3.0"></a>
## [1.3.0](https://github.com/dunbarcyber/cyphon/compare/1.2.0...1.3.0) (2017-06-28)

### Added

- Tox configuration - [PR #92](https://github.com/dunbarcyber/cyphon/pull/92) ([1299f58](https://github.com/dunbarcyber/cyphon/commit/1299f58))
- **docs:** added screenshots to overview ([f807d4a](https://github.com/dunbarcyber/cyphon/commit/f807d4a))
- **docs:** added FAQs page ([7488729](https://github.com/dunbarcyber/cyphon/commit/7488729))
- **docs:** added support page ([f022900](https://github.com/dunbarcyber/cyphon/commit/f022900))
- **docs:** added testing page to dev guide ([a9e6a4e](https://github.com/dunbarcyber/cyphon/commit/a9e6a4e))
- **docs:** added Twitter tutorial - [PR #113](https://github.com/dunbarcyber/cyphon/pull/113) ([56e7e74](https://github.com/dunbarcyber/cyphon/commit/56e7e74))
- **lab.sentiment:** added sentiment analysis - [PR #108](https://github.com/dunbarcyber/cyphon/pull/108) ([859f9b7](https://github.com/dunbarcyber/cyphon/commit/859f9b7))

### Changed

- upgraded to Django 1.11 - [PR #101](https://github.com/dunbarcyber/cyphon/pull/101) ([d4cd82b](https://github.com/dunbarcyber/cyphon/commit/d4cd82b))
- **alerts:** Alerts can be filtered by Warehouse ([19c37e9](https://github.com/dunbarcyber/cyphon/commit/19c37e9))
- **ambassador.platforms:** Platforms are ordered by name ([0381433](https://github.com/dunbarcyber/cyphon/commit/0381433))
- **bottler.tastes**: Tastes are ordered by container ([972a35c](https://github.com/dunbarcyber/cyphon/commit/972a35c))
- **contexts:** Contexts are ordered by name ([174eb81](https://github.com/dunbarcyber/cyphon/commit/174eb81))
- **parsers:** Parsers are ordered by name ([4daf0fa](https://github.com/dunbarcyber/cyphon/commit/4daf0fa))
- **sifter.condensers:** Condensers are ordered by name ([4daf0fa](https://github.com/dunbarcyber/cyphon/commit/4daf0fa))

### Fixed

- **Dockerfile**: fixed issue with proj4 library - [PR #106](https://github.com/dunbarcyber/cyphon/pull/106) ([900760d](https://github.com/dunbarcyber/cyphon/commit/900760d))
- **docs**: mocked out GDAL in Sphinx build - [PR #107](https://github.com/dunbarcyber/cyphon/pull/107) ([d1ab82e](https://github.com/dunbarcyber/cyphon/commit/d1ab82e))
- **sifter.chutes**: added Chute ID to admin list display ([2abb5f0](https://github.com/dunbarcyber/cyphon/commit/2abb5f0))
- **tests**: fixed URL for SauceLabs - [PR #112](https://github.com/dunbarcyber/cyphon/pull/112) ([a2feddd](https://github.com/dunbarcyber/cyphon/commit/a2feddd))

### Removed

- **docs:** removed list of dependencies ([b2678bb](https://github.com/dunbarcyber/cyphon/commit/b2678bb))
- **docs:** removed testing env from starter-docker.txt ([cf766b8](https://github.com/dunbarcyber/cyphon/commit/cf766b8))


<a name="1.2.0"></a>
## [1.2.0](https://github.com/dunbarcyber/cyphon/compare/1.1.3...1.2.0) (2017-06-05)

### Added

- **cyclops:** added built-in Cyclops integration ([d4baf47](https://github.com/dunbarcyber/cyphon/commit/d4baf47), [2f7f574](https://github.com/dunbarcyber/cyphon/commit/2f7f574))
- **cyphon.dashboard:** added Categories to admin dashboard ([dbfb658](https://github.com/dunbarcyber/cyphon/commit/dbfb658))
- **cyphon.dashboard:** added "Latest Cyphon News" to admin dashboard ([910f2fd](https://github.com/dunbarcyber/cyphon/commit/910f2fd))
- **cyphon.settings:** added settings for Cyclops integration ([d4baf47](https://github.com/dunbarcyber/cyphon/commit/d4baf47), [2f7f574](https://github.com/dunbarcyber/cyphon/commit/2f7f574))
- **docs:** added docs for push notifications ([1c98e3b](https://github.com/dunbarcyber/cyphon/commit/1c98e3b))
- **docs:** added docs for configuring Cyclops ([1c98e3b](https://github.com/dunbarcyber/cyphon/commit/1c98e3b))

### Changed

- **Dockerfile:** Docker image is now based on Alpine Linux ([517af76](https://github.com/dunbarcyber/cyphon/commit/517af76))
- **alarms, monitors, watchdogs:** Monitors and Watchdogs are now sorted by name ([0c98fc9](https://github.com/dunbarcyber/cyphon/commit/0c98fc9))
- **sifter:** all Rules and SieveNodes are now sorted by name ([b9128f3](https://github.com/dunbarcyber/cyphon/commit/b9128f3))

### Fixed

- **ambassador.passports:** fixed storage directory for Passport file field ([e97fd33](https://github.com/dunbarcyber/cyphon/commit/e97fd33))


<a name="1.1.3"></a>
## [1.1.3](https://github.com/dunbarcyber/cyphon/compare/1.1.2...1.1.3) (2017-05-27)

### Added

- **categories:** added REST API endpoint for Categories ([360dc56](https://github.com/dunbarcyber/cyphon/commit/360dc56))
- **docs:** added email tutorial ([d8fd982](https://github.com/dunbarcyber/cyphon/commit/d8fd982))
- **docs:** added Logstash tutorial ([69769f9](https://github.com/dunbarcyber/cyphon/commit/69769f9), [1c56516](https://github.com/dunbarcyber/cyphon/commit/1c56516))
- **docs:** added minimum system requirements ([d00b95](https://github.com/dunbarcyber/cyphon/commit/d00b95))

### Fixed

- **.gitignore:** fixed directory for Cyphon settings ([e863c4a](https://github.com/dunbarcyber/cyphon/commit/e863c4a))
- **bottler.bottles:** fixed bug with EmbeddedDocumentFields ([6fd70f5](https://github.com/dunbarcyber/cyphon/commit/6fd70f5))
- **docs:** updated instructions for Elasticsearch data directory ([03c3446](https://github.com/dunbarcyber/cyphon/commit/03c3446))


<a name="1.1.2"></a>
## [1.1.2](https://github.com/dunbarcyber/cyphon/compare/1.1.1...1.1.2) (2017-05-16)

### Fixed

- **sifter.mungers:** modified `Munger.process()` to avoid errors when processing mail ([84f8871](https://github.com/dunbarcyber/cyphon/commit/84f8871))


<a name="1.1.1"></a>
## [1.1.1](https://github.com/dunbarcyber/cyphon/compare/1.1.0...1.1.1) (2017-05-16)

### Fixed

- **alerts:** modified `Alert.save()` so that `location` and `content_date` are added the Alert to even if the Alert already has `data`, and a `title` with a default value is refreshed ([a37d9eb](https://github.com/dunbarcyber/cyphon/commit/a37d9eb))
- **alerts:** `Alert.saved_data` is no longer cached ([9fdba5d](https://github.com/dunbarcyber/cyphon/commit/9fdba5d))
- **engines.elasticsearch.engine:** Elasticsearch indexes are refreshed prior to searching by id ([65d72e2](https://github.com/dunbarcyber/cyphon/commit/65d72e2))
- **watchdogs:** Watchdogs pass data directly to Muzzles instead of fetching saved data, avoiding race condition in Logstash ([7c5a53d](https://github.com/dunbarcyber/cyphon/commit/7c5a53d))


<a name="1.1.0"></a>
## [1.1.0](https://github.com/dunbarcyber/cyphon/compare/1.0.3...1.1.0) (2017-05-14)

### Added

- **cyphon.documents:** added `DocumentOj` class for handling document references ([d701762](https://github.com/dunbarcyber/cyphon/commit/d701762))
- **receiver.receiver:** added RabbitMQ queue consumers for DataChutes, Watchdogs, and Monitors ([d701762](https://github.com/dunbarcyber/cyphon/commit/d701762))
- **target.followees:** added `get_by_natural_key()` method for Followees, Accounts, LegalNames, and Aliases ([0f8f3b8](https://github.com/dunbarcyber/cyphon/commit/0f8f3b8))
- **target.locations:** added `get_by_natural_key()` method for Locations ([2b5199d](https://github.com/dunbarcyber/cyphon/commit/2b5199d))
- **target.searchterms:** added `get_by_natural_key()` method for SearchTerms ([813c1ca](https://github.com/dunbarcyber/cyphon/commit/813c1ca))

### Fixed

- **sifter.condensers:** removed extra inline Fitting form ([10f53ce](https://github.com/dunbarcyber/cyphon/commit/10f53ce))
- **sifter.logsifter:** fixed "Test this rule" tool on LogRule admin page ([751d55b](https://github.com/dunbarcyber/cyphon/commit/751d55b))


<a name="1.0.3"></a>
## [1.0.3](https://github.com/dunbarcyber/cyphon/compare/1.0.2...1.0.3) (2017-05-14)

### Added

- **bottler:** added `get_by_natural_key()` method for BottleFields and LabelFields ([68c2a15](https://github.com/dunbarcyber/cyphon/commit/68c2a15))
- **contexts:** added `get_by_natural_key()` method for Contexts and ContextFields ([09ff0b8](https://github.com/dunbarcyber/cyphon/commit/09ff0b8))
- **cyphon.dashboard:** added Protocols and Constance to admin dashboard ([ee34361](https://github.com/dunbarcyber/cyphon/commit/ee34361), [0cbbb15](https://github.com/dunbarcyber/cyphon/commit/0cbbb15))
- **entrypoints:** added conditional for loading example fixtures ([a0efa1f](https://github.com/dunbarcyber/cyphon/commit/a0efa1f))
- **watchdogs:** added `get_by_natural_key()` method for Triggers ([8312713](https://github.com/dunbarcyber/cyphon/commit/8312713))

### Changed

- **cyphon.tests.functional_tests:** enabled functional tests to run in a Selenium 3 Docker container ([fe170cc](https://github.com/dunbarcyber/cyphon/commit/fe170cc))
- **docs:** replaced install instructions for Docker Engine with those for Docker Community Edition ([4aa080c](https://github.com/dunbarcyber/cyphon/commit/4aa080c))

### Fixed

- **responder.actions.filters:** fixed ActionFilterBackend to allow access to Actions associated with public Passports ([952464b](https://github.com/dunbarcyber/cyphon/commit/952464b))

### Removed

- **fixtures:** removed default fixtures, since these are provided in [Cyphondock](https://github.com/dunbarcyber/cyphondock/) ([ba25363](https://github.com/dunbarcyber/cyphon/commit/ba25363))

### Security

* **entrypoints**: Celery beat and worker are now run without superuser privileges ([8f18b42](https://github.com/dunbarcyber/cyphon/commit/8f18b42))


<a name="1.0.2"></a>
## [1.0.2](https://github.com/dunbarcyber/cyphon/compare/1.0.1...1.0.2) (2017-04-07)

### Added

- **docs:** added CHANGELOG ([baf76ae](https://github.com/dunbarcyber/cyphon/commit/baf76ae))

### Changed

- **docs:** changed AUTHORS to markdown ([beb0d87](https://github.com/dunbarcyber/cyphon/commit/beb0d87))

### Fixed

- **contexts:** fixed issue with ContextFilters handling nested fields ([ac58553](https://github.com/dunbarcyber/cyphon/commit/ac58553))
- **cyphon.settings:** applied fix for [django-filter issue #562](https://github.com/carltongibson/django-filter/issues/562) ([7f09009](https://github.com/dunbarcyber/cyphon/commit/7f09009))
- **engine.mongodb.engine:** fixed issue with MongoDB queries ([ea1b043](https://github.com/dunbarcyber/cyphon/commit/ea1b043))
- **watchdogs:** fixed issue with Muzzles handling nested fields ([fe30e75](https://github.com/dunbarcyber/cyphon/commit/fe30e75))


<a name="1.0.1"></a>
## [1.0.1](https://github.com/dunbarcyber/cyphon/compare/1.0.0...1.0.1) (2017-04-05)

### Changed

- **docs:** added disclaimer to securing-cyphon.txt ([39e2d65](https://github.com/dunbarcyber/cyphon/commit/39e2d65), [4cdc5e2](https://github.com/dunbarcyber/cyphon/commit/4cdc5e2), [c811257](https://github.com/dunbarcyber/cyphon/commit/c811257), [b1722c3](https://github.com/dunbarcyber/cyphon/commit/b1722c3))
- **docs:** updated favicon ([14ab3ff](https://github.com/dunbarcyber/cyphon/commit/14ab3ff))

### Fixed

- **docs:** deleted obsolete appuser docs ([ea3e5f3](https://github.com/dunbarcyber/cyphon/commit/ea3e5f3))
- **query.reservoirqueries.reservoirqueries:** fixed bug affecting Followee-based Filters ([b6a8fd9](https://github.com/dunbarcyber/cyphon/commit/b6a8fd9))


<a name="1.0.0"></a>
## [1.0.0](https://github.com/dunbarcyber/cyphon/releases/tag/1.0.0) (2017-04-04)
