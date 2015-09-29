django-netjsongraph
===================

.. image:: https://travis-ci.org/interop-dev/django-netjsongraph.png
   :target: https://travis-ci.org/interop-dev/django-netjsongraph

.. image:: https://coveralls.io/repos/interop-dev/django-netjsongraph/badge.png
  :target: https://coveralls.io/r/interop-dev/django-netjsongraph

.. image:: https://requires.io/github/interop-dev/django-netjsongraph/requirements.png?branch=master
   :target: https://requires.io/github/interop-dev/django-netjsongraph/requirements/?branch=master
   :alt: Requirements Status

.. image:: https://badge.fury.io/py/django-netjsongraph.png
   :target: http://badge.fury.io/py/django-netjsongraph

.. image:: https://img.shields.io/pypi/dm/django-netjsongraph.svg
   :target: https://pypi.python.org/pypi/django-netjsongraph

------------

Django implementation of NetJSON NetworkGraph.

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

Running tests
-------------

Install your forked repo:

.. code-block:: shell

    git clone git://github.com/<your_fork>/django-netjsongraph
    cd django-netjsongraph/
    python setup.py develop

Install test requirements:

.. code-block:: shell

    pip install -r requirements-test.txt

Run tests with:

.. code-block:: shell

    ./runtests.py

Contributing
------------

1. Announce your intentions in the `issue tracker <https://github.com/openwisp/netjsonconfig/issues>`__
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
