Changelog
=========

Version 0.6.3.post1 [2020-06-04]
--------------------------------

- [bug] fixed broken testcase in 0.6.3 release
- [change] minor changes handle post-releases in ``get_version()``

Version 0.6.3 - 2020-06-03 [YANKED]
-----------------------------------

- [add] Support of openwisp-utils~=0.5.0
- [fixed] Minor issues with testcases

Version 0.6.2 [2020-03-19]
--------------------------

- Renamed api setting ``TOPOLOGY_RECEIVE_BASEURL`` -> ``TOPOLOGY_API_BASEURL``
- Renamed api setting ``TOPOLOGY_RECEIVE_URLCONF`` -> ``TOPOLOGY_API_URLCONF``

Version 0.6.1 [2020-02-26]
--------------------------

- Added settings option TOPOLOGY_RECEIVE_URLCONF & TOPOLOGY_RECEIVE_BASEURL
- Move from jsonfield2 to jsonfield

Version 0.6.0 [2020-02-07]
--------------------------

- Dropped Python 3.5 and below
- Dropped django 2.1 and below
- Dropped netdiff 0.6 and below
- Dropped openwisp-utils 0.3 and below
- Moved ``ReceiveUrlAdmin`` & ``get_random_key`` logic to openwisp-utils
- Moved from jsonfield to jsonfield2 3.X.X
- Added Django 3.0 support
- Added netdiff 0.7 support
- Added openwisp-utils 0.4 support

Version 0.5.0 [2020-01-13]
--------------------------

- Upgraded dependencies (django and django-rest-framework)
- Changed implementation of node addresses

Version 0.4.3 [2017-02-24]
--------------------------

- `#62 <https://github.com/netjson/django-netjsongraph/pull/62>`_:
  [bug] Fixed bug related to addresses formatting
- `#77 <https://github.com/netjson/django-netjsongraph/pull/77>`_:
  [admin] Update topology action now ignores topologies with RECEIVE strategy
- `#78 <https://github.com/netjson/django-netjsongraph/pull/78>`_:
  [feature] Added automatic removal of old nodes with ``NETJSONGRAPH_NODE_EXPIRATION``

Version 0.4.2 [2017-02-19]
--------------------------

- [requirements] openwisp-utils>=0.2,<0.3

Version 0.4.1 [2017-02-19]
--------------------------

- `#82 <https://github.com/netjson/django-netjsongraph/pull/82>`_:
  [ci] Add JSLint
- `#81 <https://github.com/netjson/django-netjsongraph/pull/81>`_:
  [ci] Add pending migration check
- `#75 <https://github.com/netjson/django-netjsongraph/pull/72>`_:
  [qa] Added JSLint check
- `#73 <https://github.com/netjson/django-netjsongraph/pull/73>`_:
  [models] Added link status up/down time
- `115066 <https://github.com/netjson/django-netjsongraph/commit/115066>`_:
  Added forgotten migration

Version 0.4.0 [2017-12-28]
--------------------------

- `#72 <https://github.com/netjson/django-netjsongraph/pull/72>`_:
  [requirements] Upgrade netdiff to 0.6.0
- `e67286 <https://github.com/netjson/django-netjsongraph/commit/e67286>`_:
  [topology] Add labels when creating nodes
- `#70 <https://github.com/netjson/django-netjsongraph/pull/70>`_:
  Added support to Django 2.0
- `#67 <https://github.com/netjson/django-netjsongraph/pull/67>`_:
  [QA] Fixed flake8 errors in Travis build
- `#64 <https://github.com/netjson/django-netjsongraph/pull/64>`_:
  [requirements] Updated rest framework version
- `#60 <https://github.com/netjson/django-netjsongraph/pull/60>`_:
  [netdiff] Added support to OpenVPN parser
- `#53 <https://github.com/netjson/django-netjsongraph/pull/53>`_:
  Improved the UI of the way back machine
- `#49 <https://github.com/netjson/django-netjsongraph/pull/49>`_:
  Added Topology history feature

Version 0.3.4 [2017-08-19]
--------------------------

- `7ea174 <https://github.com/netjson/django-netjsongraph/commit/7ea174>`_:
  Minor simplification in update_all
- `#51 <https://github.com/netjson/django-netjsongraph/pull/51>`_:
  [templates] Made node template reusable

Version 0.3.3 [2017-07-22]
--------------------------

- `#42 <https://github.com/netjson/django-netjsongraph/pull/42>`_:
  Made test-api, topology update function and update command reusable
- `#44 <https://github.com/netjson/django-netjsongraph/pull/44>`_:
  Made test-utils reusable
- `#45 <https://github.com/netjson/django-netjsongraph/pull/45>`_:
  Made test-admin reusable
- `e5642c <https://github.com/netjson/django-netjsongraph/commit/e5642c>`_:
  [admin] Added search for Topology model
- `#48 <https://github.com/netjson/django-netjsongraph/pull/48>`_:
   Moved all the reusable tests to tests.base and separated into files

Version 0.3.2 [2017-07-10]
--------------------------

- `#39 <https://github.com/netjson/django-netjsongraph/pull/39>`_:
  Upgraded to django 1.11
- `891e58 <https://github.com/netjson/django-netjsongraph/commit/891e58>`_:
  [admin] Moved submit_line.html to openwisp_utils

Version 0.3.1 [2017-06-22]
--------------------------

- `fefbce5 <https://github.com/netjson/django-netjsongraph/commit/fefbce5>`_:
  [visualizer] Provided base classes to improve reusability
- `a0c4cc7 <https://github.com/netjson/django-netjsongraph/commit/a0c4cc7>`_:
  Added netjsongraph.js visualization to admin site

Version 0.3.0 [2017-05-31]
--------------------------

- `#24 <https://github.com/netjson/django-netjsongraph/issues/24>`_:
  Provided base classes to improve reusability
- `#27 <https://github.com/netjson/django-netjsongraph/issues/27>`_:
  [link] Added ``link_status_changed`` signal
- `#15 <https://github.com/netjson/django-netjsongraph/issues/15>`_:
  Added ``NETJSONGRAPH_VISUALIZER_CSS`` setting and instructions to override default templates

Version 0.2.3 [2017-05-18]
--------------------------

- `#17 <https://github.com/netjson/django-netjsongraph/issues/17>`_:
  Updated django-rest-framework version requirement
- `#22 <https://github.com/netjson/django-netjsongraph/issues/22>`_:
  Added support for Django 1.11
- `#18 <https://github.com/netjson/django-netjsongraph/issues/18>`_:
  [QA] Added flake8 and isort checks to travis-ci build
- `#9 <https://github.com/netjson/django-netjsongraph/issues/9>`_:
  Added a way to easily copy API endpoint URL when using RECEIVE strategy

Version 0.2.2 [2016-12-14]
--------------------------

- `#16 <https://github.com/netjson/django-netjsongraph/issues/16>`_:
  added support for django 1.10.x
- `9ce1b15 <https://github.com/netjson/django-netjsongraph/commit/9ce1b15>`_:
  [JS] Updated d3 to 3.5.17

Version 0.2.1 [2016-05-20]
--------------------------

- `f3fa59f <https://github.com/netjson/django-netjsongraph/commit/f3fa59f>`_:
  [admin] fixed name mismatch in "Links to other nodes"
- `#10 <https://github.com/netjson/django-netjsongraph/issues/10>`_:
  fixed visualizer: removed accidental ignore of d3.js

Version 0.2.0 [2016-01-24]
--------------------------

- `#5 <https://github.com/netjson/django-netjsongraph/issues/5>`_:
  added support for receiving topology from nodes
- `#6 <https://github.com/netjson/django-netjsongraph/issues/6>`_:
  avoid failures if ``addresses`` field is too long
- `#7 <https://github.com/netjson/django-netjsongraph/issues/7>`_:
  stricter lookups in ``get_from_address``, ``get_from_nodes``, ``count_address``

Version 0.1.3 [2016-01-09]
--------------------------

- `#4 <https://github.com/netjson/django-netjsongraph/issues/4>`_:
  pevented ``ValueError`` in ``topology_detail`` view

Version 0.1.2 [2016-01-04]
--------------------------

- `19a1f6a <https://github.com/netjson/django-netjsongraph/commit/19a1f6a>`_:
  added ``NETJSONGRAPH_TIMEOUT``
- `365509c <https://github.com/netjson/django-netjsongraph/commit/365509c>`_:
  avoided possible *500 internal server error* when updating topology from admin action
- `7fa86db <https://github.com/netjson/django-netjsongraph/commit/7fa86db>`_:
  added failure message when updating topology from admin
- `56066e8 <https://github.com/netjson/django-netjsongraph/commit/56066e8>`_:
  added ``get_absolute_url()`` method to ``Topology`` model
- `f90c639 <https://github.com/netjson/django-netjsongraph/commit/f90c639>`_:
  added "Links to other nodes" section in ``Node`` admin
- `d6fff61 <https://github.com/netjson/django-netjsongraph/commit/d6fff61>`_:
  added ``NETJSONGRAPH_LINK_EXPIRATION`` days setting
- `#3 <https://github.com/netjson/django-netjsongraph/issues/3>`_,
  `b246669 <https://github.com/netjson/django-netjsongraph/commit/b246669>`_:
  minor improvements to visualizer

Version 0.1.1 [2015-12-27]
--------------------------

- added possibility to unpublish topologies
- added admin actions for topology admin: unpublish, publish and update
- update topology attributes (protocol, version, metric) when latest data is retrieved
- improved update method of ``Topology`` model

Version 0.1 [2015-12-23]
------------------------

- topology collector
- HTTP API
- visualizer
- admin
