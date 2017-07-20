django-netjsongraph
===================

.. image:: https://travis-ci.org/netjson/django-netjsongraph.svg
   :target: https://travis-ci.org/netjson/django-netjsongraph

.. image:: https://coveralls.io/repos/netjson/django-netjsongraph/badge.svg
  :target: https://coveralls.io/r/netjson/django-netjsongraph

.. image:: https://requires.io/github/netjson/django-netjsongraph/requirements.svg?branch=master
   :target: https://requires.io/github/netjson/django-netjsongraph/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/django-netjsongraph.svg
   :target: http://badge.fury.io/py/django-netjsongraph

------------

Reusable django app for collecting and visualizing network topology.

.. image:: https://raw.githubusercontent.com/netjson/django-netjsongraph/master/docs/images/visualizer.png

.. image:: https://raw.githubusercontent.com/netjson/django-netjsongraph/master/docs/images/admin.png

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
* **network topology visualizer** based on `netjsongraph.js <https://github.com/netjson/netjsongraph.js>`_
* **simple HTTP API** that exposes data in `NetJSON <http://netjson.org>`__ *NetworkGraph* format
* **admin interface** that allows to easily manage, audit, visualize and debug topologies and their relative data (nodes, links)
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

Deploy it in production
-----------------------

An automated installer is provided by the `OpenWISP <http://openwisp.org>`_ project:
`ansible-openwisp2 <https://github.com/openwisp/ansible-openwisp2>`_.

Ensure to follow the instructions explained in the following section: `Enabling the network topology
module <https://github.com/openwisp/ansible-openwisp2#enabling-the-network-topology-module>`_.

Install stable version from pypi
--------------------------------

Install from pypi:

.. code-block:: shell

    pip install django-netjsongraph

Install development version
---------------------------

Install tarball:

.. code-block:: shell

    pip install https://github.com/netjson/django-netjsongraph/tarball/master

Alternatively you can install via pip using git:

.. code-block:: shell

    pip install -e git+git://github.com/netjson/django-netjsongraph#egg=django-netjsongraph

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
        'openwisp_utils.admin_theme',
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
<https://github.com/netjson/django-netjsongraph/blob/master/tests/settings.py#L66>`_.

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

``NETJSONGRAPH_VISUALIZER_CSS``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------+--------------------------------+
| **type**:    | ``str``                        |
+--------------+--------------------------------+
| **default**: | ``netjsongraph/css/style.css`` |
+--------------+--------------------------------+

Path of the visualizer css file. Allows customization of css according to user's
preferences.

Overriding visualizer templates
-------------------------------

Follow these steps to override and customise the visualizer's default templates:

* create a directory in your django project and put its full path in ``TEMPLATES['DIRS']``,
  which can be found in the django ``settings.py`` file
* create a sub directory named ``netjsongraph`` and add all the templates which shall override
  the default ``netjsongraph/*`` templates
* create a template file with the same name of the template file you want to override

More information about the syntax used in django templates can be found in the `django templates
documentation <https://docs.djangoproject.com/en/dev/ref/templates/>`_.

Example: overriding the ``<script>`` tag
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's a step by step guide on how to change the javascript options passed to `netjsongraph.js
<https://github.com/netjson/netjsongraph.js>`_, remember to replace ``<project_path>`` with the
absolute filesytem path of your project.

**Step 1**: create a directory in ``<project_path>/templates/netjsongraph``

**Step 2**: open your ``settings.py`` and edit the ``TEMPLATES['DIRS']`` setting so that it looks
like the following example:

.. code-block:: python

    # settings.py
    TEMPLATES = [
        {
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            # ... all other lines have been omitted for brevity ...
        }
    ]

**Step 3**: create a new file named ``netjsongraph-script.html`` in
the new ``<project_path>/templates/netjsongraph/`` directory, eg:

.. code-block:: html

    <!-- <project_path>/templates/netjsongraph/netjsongraph-script.html -->
    <script>
        var graph = d3.netJsonGraph("{% url 'network_graph' topology.pk %}", {
            linkClassProperty: "status",
            defaultStyle: false,
            labelDy: "-1.4em",
            circleRadius: 8,
            charge: -100,
            gravity: 0.3,
            linkDistance: 100,
            linkStrength: 0.2,
            # more customisations here ...
        });
    </script>

Extending django-netjsongraph
-----------------------------

*django-netjsongraph* provides a set of models, admin classes and generic views which can be imported, extended and reused by third party apps.

To extend *django-netjsongraph*, **you MUST NOT** add it to ``settings.INSTALLED_APPS``, but you must create your own app (which goes into ``settings.INSTALLED_APPS``), import the base classes from django-netjsongraph and add your customizations.

Extending models
^^^^^^^^^^^^^^^^

This example provides an example of how to extend the base models of
*django-netjsongraph*.

.. code-block:: python

    # models.py of your custom ``network`` app
    from django.db import models

    from django_netjsongraph.base.link import AbstractLink
    from django_netjsongraph.base.node import AbstractNode
    from django_netjsongraph.base.topology import AbstractTopology

    # the model ``organizations.Organization`` is omitted for brevity
    # if you are curious to see a real implementation, check out django-organizations
    # https://github.com/bennylope/django-organizations

    class OrganizationMixin(models.Model):
        organization = models.ForeignKey('organization.Organization')

        class Meta:
            abstract = True


    class Topology(OrganizationMixin, AbstractTopology):
        def clean(self):
            # your own validation logic here
            pass

        class Meta(AbstractTopology.Meta):
            abstract = False


    class Node(AbstractNode):
        topology = models.ForeignKey('Topology')

        class Meta:
            abstract = False


    class Link(AbstractLink):
        topology = models.ForeignKey('Topology')
        source = models.ForeignKey('Node',
                                   related_name='source_link_set')
        target = models.ForeignKey('Node',
                                   related_name='source_target_set')

        class Meta:
            abstract = False

Extending the admin
^^^^^^^^^^^^^^^^^^^

Following the above example, you can avoid duplicating the admin code by importing the base admin classes and registering your models with.

.. code-block:: python

    # admin.py of your app
    from django.contrib import admin
    from django_netjsongraph.base.admin import (AbstractLinkAdmin,
                                                AbstractNodeAdmin,
                                                AbstractTopologyAdmin)
    # these are you custom models
    from .models import Link, Node, Topology


    class TopologyAdmin(AbstractTopologyAdmin):
        model = Topology


    class NodeAdmin(AbstractNodeAdmin):
        model = Node


    class LinkAdmin(AbstractLinkAdmin):
        model = Link


    admin.site.register(Link, LinkAdmin)
    admin.site.register(Node, NodeAdmin)
    admin.site.register(Topology, TopologyAdmin)

Extending API views
^^^^^^^^^^^^^^^^^^^

If your use case doesn't vary much from the base, you may also want to try to reuse the API views:

.. code-block:: python

    # your app.api.views
    from ..models import Topology
    from django_netjsongraph.api.generics import (BaseNetworkCollectionView,
                                                  BaseNetworkGraphView,
                                                  BaseReceiveTopologyView)


    class NetworkCollectionView(BaseNetworkCollectionView):
        queryset = Topology.objects.filter(published=True)


    class NetworkGraphView(BaseNetworkGraphView):
        queryset = Topology.objects.filter(published=True)


    class ReceiveTopologyView(BaseReceiveTopologyView):
        model = Topology


    network_collection = NetworkCollectionView.as_view()
    network_graph = NetworkGraphView.as_view()
    receive_topology = ReceiveTopologyView.as_view()

API URLs
^^^^^^^^

If you are not making drastic changes to the api views, you can avoid duplicating the URL logic by using the ``get_api_urls`` function. Put this in your api ``urls.py``:

.. code-block:: python

    # your app.api.urls
    from django_netjsongraph.utils import get_api_urls
    from . import views

    urlpatterns = get_api_urls(views)

Extending Visualizer Views
^^^^^^^^^^^^^^^^^^^^^^^^^^
If your use case doesn't vary much from the base, you may also want to try to reuse the Visualizer views:

.. code-block:: python

    # your app.visualizer.views
    from ..models import Topology
    from .generics import BaseTopologyDetailView, BaseTopologyListView


    class TopologyListView(BaseTopologyListView):
        topology_model = Topology


    class TopologyDetailView(BaseTopologyDetailView):
        topology_model = Topology


    topology_list = TopologyListView.as_view()
    topology_detail = TopologyDetailView.as_view()


Visualizer URLs
^^^^^^^^^^^^^^^
If you are not making any drastic changes to visualizer views, you can avoid duplicating the URL logic by using ``get_visualizer_urls`` function. Put this in your visualizer ``urls.py``

.. code-block:: python

    # your app.visualizer.urls
    from django_netjsongraph.utils import get_visualizer_urls
    from . import views

    urlpatterns = get_visualizer_urls(views)

Extending AppConfig
^^^^^^^^^^^^^^^^^^^

You may want to reuse the ``AppConfig`` class of *django-netjsongraph* too:

.. code-block:: python

    from django_netjsongraph.apps import DjangoNetjsongraphConfig

    class MyOwnConfig(DjangoNetjsongraphConfig):
        name = 'yourapp'
        label = 'yourapp'

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
   `issue tracker <https://github.com/netjson/django-netjsongraph/issues>`_
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

See `CHANGES <https://github.com/netjson/django-netjsongraph/blob/master/CHANGES.rst>`_.

License
-------

See `LICENSE <https://github.com/netjson/django-netjsongraph/blob/master/LICENSE>`_.

This projects bundles third-party javascript libraries in its source code:

- `D3.js (BSD-3-Clause) <https://github.com/netjson/django-netjsongraph/blob/master/django_netjsongraph/static/netjsongraph/lib/d3.min.js>`_
