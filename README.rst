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

------------

Current features:

* topology information collector supporting different formats:
    - NetJSON NetworkGraph
    - OLSR (jsoninfo/txtinfo)
    - batman-adv (jsondoc/txtinfo)
    - BMX6 (q6m)
    - CNML 1.0
* **visualizer** based on `netjsongraph.js <https://github.com/interop-dev/netjsongraph.js>`_
* **simple HTTP API** that exposes data in `NetJSON <http://netjson.org>`__ *NetworkGraph* format

Goals:

* make it easy to visualize network topology data for the formats supported by `netdiff <https://github.com/ninuxorg/netdiff>`_
* expose topology data via RESTful resources in *NetJSON NetworkGraph* format
* make it easy to integrate in larger django projects to improve reusability
* make it easy to extend its models by providing abstract models (**needs improvement in this point**)
* provide ways to customize or replace the visualizer (**needs improvement in this point**)
* keep the core very simple, provide ways to extend the default behaviour

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

Settings
--------

+----------------------------------+-------------------------------------+---------------------------------------------------------------------------------------------------+
| Setting                          | Default value                       | Description                                                                                       |
+==================================+=====================================+===================================================================================================+
| ``NETJSONGRAPH_PARSERS``         | ``[]``                              | List with additional custom `netdiff parsers <https://github.com/ninuxorg/netdiff#parsers>`_      |
+----------------------------------+-------------------------------------+---------------------------------------------------------------------------------------------------+
| ``NETJSONGRAPH_SIGNALS``         | ``None``                            | String representing python module to import on initialization.                                    |
|                                  |                                     | Useful for loading django signals or to define custom behaviour.                                  |
+----------------------------------+-------------------------------------+---------------------------------------------------------------------------------------------------+
| ``NETJSONGRAPH_TIMEOUT``         | ``8``                               | Timeout when requesting topology URLs                                                             |
+----------------------------------+-------------------------------------+---------------------------------------------------------------------------------------------------+
| ``NETJSONGRAPH_LINK_EXPIRATION`` | ``60``                              | If a link is down for more days than this number, it will be deleted by the ``update_topology``   |
|                                  |                                     | management command. Setting this to ``False`` will disable this feature.                          |
+----------------------------------+-------------------------------------+---------------------------------------------------------------------------------------------------+

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

1. Announce your intentions in the `issue tracker <https://github.com/interop-dev/django-netjsongraph/issues>`__
2. Fork this repo and install it
3. Follow `PEP8, Style Guide for Python Code`_
4. Write code
5. Write tests for your code
6. Ensure all tests pass
7. Ensure test coverage is not under 90%
8. Document your changes
9. Send pull request

.. _PEP8, Style Guide for Python Code: http://www.python.org/dev/peps/pep-0008/
.. _ninux-dev mailing list: http://ml.ninux.org/mailman/listinfo/ninux-dev
