django-netjsongraph
===================

**WARNING**: The development of this project has moved to `openwisp-network-topology <https://github.com/openwisp/openwisp-network-topology>`_, we advise all users of *django-netjsongraph* to follow the tutorial below to migrate their existing database:

1. Take a backup of your database.
2. Create JSON backup of data that's required for migration with the following command:

.. code-block:: shell

    # Go to the django-netjsongraph repository (or installed app)
    cd tests/
    python manage.py dumpdata auth.user > user.json
    python manage.py dumpdata auth.group > group.json
    python manage.py dumpdata django_netjsongraph > netjsongraph.json
    python manage.py dumpdata auth.permission > permission.json
    python manage.py dumpdata contenttypes > contenttype.json
    pwd # copy output of the command

3. `Setup openwisp-network-topology <https://github.com/openwisp/openwisp-network-topology#setup-integrate-in-an-existing-django-project>`_

4. `Use the upgrader script <https://github.com/openwisp/openwisp-network-topology#upgrade-from-django-netjsongraph>`_:

.. code-block:: shell

    # In the openwisp-network-topology repository
    python tests/manage.py upgrade_from_django_netjsongraph --backup <output-copied-in-step-2>

For any support, please reach out to us on `the chat channel on gitter <https://gitter.im/openwisp/general>`_ or `use the mailing list <https://groups.google.com/forum/#!forum/openwisp>`_.

**The development of django-netjsongraph is discontinued and this repository is archived.**
