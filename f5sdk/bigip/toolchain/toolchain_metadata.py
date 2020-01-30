"""Python module for BIG-IP toolchain metadata client"""

import os
import json
import re

from f5sdk.logger import Logger
from f5sdk.utils import http_utils
from f5sdk.exceptions import InvalidComponentError, InvalidComponentVersionError, FileLoadError

TOOLCHAIN_METADATA = {
    'FILE': 'toolchain_metadata.json',
    'URL': 'https://cdn.f5.com/product/cloudsolutions/f5-extension-metadata/latest/metadata.json'
}


class MetadataClient(object):
    """A class used as a metadata client

    Attributes
    ----------
    component : str
        the component in the toolchain
    version : str
        the component version in the toolchain
    toolchain_metadata : dict
        the toolchain metadata

    Methods
    -------
    get_download_url()
        Refer to method documentation
    get_package_name()
        Refer to method documentation
    get_endpoints()
        Refer to method documentation
    """

    def __init__(self, component, version, **kwargs):
        """Class initialization

        Parameters
        ----------
        component : str
            the component in the toolchain
        version : str
            the component version in the toolchain
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        use_latest_metadata : bool
            use latest metadata (will be retrieved from remote CDN)

        Returns
        -------
        None
        """

        self.logger = Logger(__name__).get_logger()

        self.use_latest_metadata = kwargs.pop('use_latest_metadata', True)
        self.toolchain_metadata = self._load_metadata()
        self.component = self._validate_component(component)
        self.version = self._validate_component_version(
            self.component,
            version or self.get_latest_version()
        )

    def _load_metadata(self):
        """Load toolchain metadata

        Load metadata using the follow order:
        - metadata from CDN (unless use_latest_metadata=False)
        - metadata included in package (local file)

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containg the JSON metadata
        """

        metadata = None

        # retrieve metadata from URL - unless opted out
        if self.use_latest_metadata:
            parsed_url = http_utils.parse_url(TOOLCHAIN_METADATA['URL'])
            try:
                metadata = http_utils.make_request(parsed_url['host'], parsed_url['path'])
            except Exception as err:  # pylint: disable=broad-except
                self.logger.warning('Error downloading metadata file: %s', err)

        # fallback to local metadata file
        if metadata is None:
            local_file = os.path.join(os.path.dirname(__file__), TOOLCHAIN_METADATA['FILE'])
            try:
                with open(local_file) as m_file:
                    metadata = json.loads(m_file.read())
            except Exception as err:  # pylint: disable=broad-except
                raise FileLoadError(err)

        return metadata

    def _validate_component(self, component):
        """Validates the toolchain component exists in metadata

        Parameters
        ----------
        component : str
            a toolchain component to check

        Returns
        -------
        str
            the toolchain component provided if it exists (see Raises)

        Raises
        ------
        Exception
            if the toolchain component does not exist in metadata
        """

        components = list(self.toolchain_metadata['components'].keys())
        if not [i for i in components if i == component]:
            raise InvalidComponentError('Valid component must be provided: %s' % (components))
        return component

    def _validate_component_version(self, component, version):
        """Validates the toolchain component version exists in metadata

        Parameters
        ----------
        component : str
            a toolchain component to check
        version : str
            a toolchain component version to check

        Returns
        -------
        str
            the toolchain component version provided if it exists (see Raises)

        Raises
        ------
        Exception
            if the toolchain component version does not exist in metadata
        """

        versions = list(self.toolchain_metadata['components'][component]['versions'].keys())
        if not [i for i in versions if i == version]:
            raise InvalidComponentVersionError(
                'Valid component version must be provided: %s' % (versions)
            )
        return version

    def _get_component_metadata(self):
        """Gets the metadata for a specific component from the toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the metadata
        """

        return self.toolchain_metadata['components'][self.component]

    def _get_version_metadata(self):
        """Gets the metadata for a specific component version from the toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the metadata
        """

        return self.toolchain_metadata['components'][self.component]['versions'][self.version]

    def get_latest_version(self):
        """Gets the latest component version from the toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the latest version
        """

        c_v_metadata = self.toolchain_metadata['components'][self.component]['versions']
        latest = {k: v for (k, v) in c_v_metadata.items() if v['latest']}
        return list(latest.keys())[0]  # we should only have one

    def get_download_url(self):
        """Gets the component versions download url from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the download url
        """

        return self._get_version_metadata()['downloadUrl']

    def get_package_name(self):
        """Gets the component versions package name from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the package name
        """

        return self._get_version_metadata()['packageName']

    def get_component_package_name(self):
        """Gets the component's package name from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the component's package name. Example: 'telemetry'
        """

        return re.split('-[0-9]',
                        re.split('f5-?', self._get_version_metadata()['packageName'])[1])[0]

    def get_endpoints(self):
        """Gets the component endpoints from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the endpoints
        """

        return self._get_component_metadata()['endpoints']
