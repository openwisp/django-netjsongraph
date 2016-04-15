django-netjsongraph
===================

.. image:: https://travis-ci.org/interop-dev/django-netjsongraph.svg
   :target: https://travis-ci.org/interop-dev/django-netjsongraph

.. image:: https://coveralls.io/repos/interop-dev/django-netjsongraph/badge.svg
  :target: https://coveralls.io/r/interop-dev/django-netjsongraph

.. image:: https://requires.io/github/interop-dev/django-netjsongraph/requirements.svg?branch=master
   :target: https://requires.io/github/interop-dev/django-netjsongraph/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/django-netjsongraph.svg
   :target: http://badge.fury.io/py/django-netjsongraph

.. image:: https://img.shields.io/pypi/dm/django-netjsongraph.svg
   :target: https://pypi.python.org/pypi/django-netjsongraph

------------

Reusable django app for collecting and visualizing network topology.

.. image:: https://raw.githubusercontent.com/interop-dev/django-netjsongraph/master/docs/images/visualizer.png

.. image:: https://raw.githubusercontent.com/interop-dev/django-netjsongraph/master/docs/images/admin.png

.. contents:: **Table of Contents**:
   :backlinks: none
   :depth: 3

------------

Current features
----------------

* **network topology collector** supporting different formats:
    - NetJSON NetworkGraph
    - OLSR (jsoninfo/txtinfo)
    - batman-adv (jsondoc/txtinfo)
    - BMX6 (q6m)
    - CNML 1.0
    - additional formats can be added by `specifying custom parsers <#netjsongraph-parsers>`_
* **network topology visualizer** based on `netjsongraph.js <https://github.com/interop-dev/netjsongraph.js>`_
* **simple HTTP API** that exposes data in `NetJSON <http://netjson.org>`__ *NetworkGraph* format
* **admin interface** that allows to easily manage, audit and debug topologies and their relative data (nodes, links)
* **receive topology** from multiple nodes

Project goals
-------------

* make it easy to visualize network topology data for the formats supported by `netdiff <https://github.com/ninuxorg/netdiff>`_
* expose topology data via RESTful resources in *NetJSON NetworkGraph* format
* make it easy to integrate in larger django projects to improve reusability
* make it easy to extend its models by providing abstract models (**needs improvement in this point**)
* provide ways to customize or replace the visualizer (**needs improvement in this point**)
* keep the core very simple
* provide ways to extend the default behaviour
* encourage new features to be published as extensions

Install stable version from pypi
--------------------------------

Install from pypi:

.. code-block:: shell

    pip install django-netjsongraph

Install development version
---------------------------

Install tarball:

.. code-block:: shell

    pip install https://github.com/interop-dev/django-netjsongraph/tarball/master

Alternatively you can install via pip using git:

.. code-block:: shell

    pip install -e git+git://github.com/interop-dev/django-netjsongraph#egg=django-netjsongraph

If you want to contribute, install your cloned fork:

.. code-block:: shell

    git clone git@github.com:<your_fork>/django-netjsongraph.git
    cd django-netjsongraph
    python setup.py develop

Setup (integrate in an existing django project)
-----------------------------------------------

Add ``rest_framework`` and ``django_netjsongraph`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # other apps
        'rest_framework',
        'django_netjsongraph'
        # ...
    ]

Include urls in your urlconf (you can change the prefixes
according to your needs):

.. code-block:: python

    from django.conf.urls import include, url

    from django_netjsongraph.api import urls as netjsongraph_api
    from django_netjsongraph.visualizer import urls as netjsongraph_visualizer

    urlpatterns = [
        # your URLs ...
        url(r'^api/', include(netjsongraph_api)),
        url(r'', include(netjsongraph_visualizer)),
    ]

Create database tables::

    ./manage.py migrate

Management Commands
-------------------

``update_topology``
^^^^^^^^^^^^^^^^^^^

After topology URLs (URLs exposing the files that the topology of the network) have been
added in the admin, the ``update_topology`` management command can be used to collect data
and start playing with the network graph::

    ./manage.py update_topology

The management command accepts a ``--label`` argument that will be used to search in
topology labels, eg::

    ./manage.py update_topology --label mytopology

Logging
-------

The ``update_topology`` management command will automatically try to log errors.

For a good default ``LOGGING`` configuration refer to the `test settings
<https://github.com/interop-dev/django-netjsongraph/blob/master/tests/settings.py#L66>`_.

Strategies
----------

There are mainly two ways of collecting topology information:

* **FETCH** strategy
* **RECEIVE** strategy

Each ``Topology`` instance has a ``strategy`` field which can be set to the desired setting.

FETCH strategy
^^^^^^^^^^^^^^

Topology data will be fetched from a URL.

When some links are not detected anymore they will be flagged as "down" straightaway.

RECEIVE strategy
^^^^^^^^^^^^^^^^

Topology data is sent directly from one or more nodes of the network.

The collector waits to receive data in the payload of a POST HTTP request;
when such a request is received, a ``key`` parameter it's first checked against
the ``Topology`` key.

If the request is authorized the collector proceeds to update the topology.

If the data is sent from one node only, it's highly advised to set the
``expiration_time`` of the ``Topology`` instance to ``0`` (seconds), this way the
system works just like in the **FETCH strategy**, with the only difference that
the data is sent by one node instead of fetched by the collector.

If the data is sent from multiple nodes, you **SHOULD** set the ``expiration_time``
of the ``Topology`` instance to a value slightly higher than the interval used
by nodes to send the topology, this way links will be flagged as "down" only if
they haven't been detected for a while. This mechanism allows to visualize the
topology even if the network has been split in several parts, the disadvantage
is that it will take a bit more time to detect links that go offline.

Settings
--------

``NETJSONGRAPH_PARSERS``
^^^^^^^^^^^^^^^^^^^^^^^^

+--------------+-------------+
| **type**:    | ``list``    |
+--------------+-------------+
| **default**: | ``[]``      |
+--------------+-------------+

Additional custom `netdiff parsers <https://github.com/ninuxorg/netdiff#parsers>`_.

``NETJSONGRAPH_SIGNALS``
^^^^^^^^^^^^^^^^^^^^^^^^

+--------------+-------------+
| **type**:    | ``str``     |
+--------------+-------------+
| **default**: | ``None``    |
+--------------+-------------+

String representing python module to import on initialization.

Useful for loading django signals or to define custom behaviour.

``NETJSONGRAPH_TIMEOUT``
^^^^^^^^^^^^^^^^^^^^^^^^

+--------------+-------------+
| **type**:    | ``int``     |
+--------------+-------------+
| **default**: | ``8``       |
+--------------+-------------+

Timeout when fetching topology URLs.

``NETJSONGRAPH_LINK_EXPIRATION``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------+-------------+
| **type**:    | ``int``     |
+--------------+-------------+
| **default**: | ``60``      |
+--------------+-------------+

If a link is down for more days than this number, it will be deleted by the
``update_topology`` management command.

Setting this to ``False`` will disable this feature.

Installing for development
--------------------------

Install sqlite:

.. code-block:: shell

    sudo apt-get install sqlite3 libsqlite3-dev

Install your forked repo:

.. code-block:: shell

    git clone git://github.com/<your_fork>/django-netjsongraph
    cd django-netjsongraph/
    python setup.py develop

Install test requirements:

.. code-block:: shell

    pip install -r requirements-test.txt

Create database:

.. code-block:: shell

    cd tests/
    ./manage.py migrate
    ./manage.py createsuperuser

Launch development server:

.. code-block:: shell

    ./manage.py runserver

You can access the visualizer at http://127.0.0.1:8000/
and the admin interface at http://127.0.0.1:8000/admin/.

Run tests with:

.. code-block:: shell

    ./runtests.py

Contributing
------------

First off, thanks for taking the time to read these guidelines.

Trying to follow these guidelines is important in order to minimize waste and
avoid misunderstandings.

1. Ensure your changes meet the `Project Goals`_
2. If you found a bug please send a failing test with a patch
3. If you want to add a new feature, announce your intentions in the
   `issue tracker <https://github.com/interop-dev/django-netjsongraph/issues>`_
4. Fork this repo and install it by following the instructions in
   `Installing for development`_
5. Follow `PEP8, Style Guide for Python Code`_
6. Write code
7. Write tests for your code
8. Ensure all tests pass
9. Ensure test coverage is not under 90%
10. Document your changes
11. Send pull request

.. _PEP8, Style Guide for Python Code: http://www.python.org/dev/peps/pep-0008/
.. _ninux-dev mailing list: http://ml.ninux.org/mailman/listinfo/ninux-dev

Changelog
---------

See `CHANGES <https://github.com/interop-dev/django-netjsongraph/blob/master/CHANGES.rst>`_.

License
-------

See `LICENSE <https://github.com/interop-dev/django-netjsongraph/blob/master/LICENSE>`_.
