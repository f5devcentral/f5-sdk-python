Quick Start
===========

Prerequisites
-------------

- Python 3.x, for installation see `python download docs <https://www.python.org/downloads/>`_.
- Python virtual environment, for details see `python venv docs <https://docs.python.org/3/tutorial/venv.html>`_.
- Optional: Specify the log level verbosity to see additional log messages during SDK usage.  See the :ref:`troubleshooting` section for more details.
- Optional: Ignore untrusted TLS certificate warnings during HTTPS requests to BIG-IP.  See the :ref:`troubleshooting` section for more details.

Installation
------------

::

    pip install f5-sdk-python --extra-index-url https://***REMOVED***/artifactory/api/pypi/f5-cloud-solutions-pypi/simple


.. note::
    Typically, all that is required to use the SDK is a basic installation.  For certain platforms or system configurations it may be simpler to get started in a container.

    ::

        docker run --rm -it -v $(pwd):/f5sdk python:3.7 /bin/bash

Usage
-----

This script uses the SDK to update BIG-IP L4-L7 configuration using AS3, provided via a local file.

For an example AS3 declaration, see the documentation `here <https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/userguide/examples.html#example-1-simple-http-application>`_.

::

    python example.py

.. literalinclude:: ../../examples/extension_as3.py
   :language: python