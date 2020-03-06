.. _troubleshooting:

Troubleshooting
===============

Enable Debugging
----------------

Debugging can be enabled by setting the following environment variable prior to using the SDK.

::

    export F5_SDK_LOG_LEVEL='DEBUG'

Ignore HTTPS warnings
---------------------

To ignore HTTPS warnings while the SDK is making HTTP requests, set the following environment variable prior to using the SDK.

::

    export PYTHONWARNINGS="ignore:Unverified HTTPS request"

.. note::
    This is not recommended for production use, please configure the BIG-IP with a valid certificate.

Alternate Management Port
-------------------------

To connect to a BIG-IP using a non-default management port, such as 8443, it should be provided during management client instantiation.

::

    device = ManagementClient('192.0.2.10', user='admin', password='admin', port=8443)

.. note::
    The BIG-IP management client will attempt to discover the management port using the order **443 > 8443 > 443 (fallback)**.  However this may result in an unwanted delay for BIG-IPs using 8443 as a management port.


|

.. include:: /_static/reuse/feedback.rst