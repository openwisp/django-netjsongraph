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

Django implementation of `NetJSON <http://netjson.org>`__ NetworkGraph.

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

    # your other imports ...

    from django_netjsongraph.rest_framework import urls as rest_urls
    from django_netjsongraph.visualizer import urls as netjsongraph_urls

    urlpatterns = [
        # your URLs ...
        url(r'^api/', include(rest_urls)),  # NetJSON API
        url(r'', include(netjsongraph_urls)),
    ]

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
