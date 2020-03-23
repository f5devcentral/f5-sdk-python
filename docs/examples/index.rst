Examples
========

The following are examples that can be followed to get up and running with the SDK.

.. note::
    These examples exist in the project source under the examples directory.


Prerequisites
-------------

- Python 3.x, for installation see `python download docs <https://www.python.org/downloads/>`_.
- Python virtual environment, for details see `python venv docs <https://docs.python.org/3/tutorial/venv.html>`_.
- Optional: Specify the log level verbosity to see additional log messages during SDK usage.  See the :ref:`troubleshooting` section for more details.
- Optional: Ignore untrusted TLS certificate warnings during HTTPS requests to BIG-IP.  See the :ref:`troubleshooting` section for more details.

Configure AS3
-------------

This script uses the SDK to update BIG-IP L4-L7 configuration using AS3, provided via a local file.

::

    python example.py

.. literalinclude:: ../../examples/extension_as3.py
   :language: python

Get F5 Cloud Services Configuration
-----------------------------------

This script uses the SDK to get F5 Cloud Services configuration.

::

    python example.py

.. literalinclude:: ../../examples/cs.py
   :language: python

Revoke License from BIG-IQ
--------------------------

This script uses the SDK to revoke a licensed BIG-IP (unreachable) from a BIG-IQ license pool.

::

    python example.py

.. literalinclude:: ../../examples/bigiq_revoke_license.py
   :language: python

|

.. include:: /_static/reuse/feedback.rst