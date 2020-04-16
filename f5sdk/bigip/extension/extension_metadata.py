"""Python module for BIG-IP extension metadata client"""

import os
import json
import re

from f5sdk.logger import Logger
from f5sdk.utils import http_utils
from f5sdk.exceptions import InvalidComponentError, InvalidComponentVersionError, FileLoadError

EXTENSION_METADATA = {
    'FILE': 'extension_metadata.json',
    'URL': 'https://cdn.f5.com/product/cloudsolutions/f5-extension-metadata/latest/metadata.json'
}


class MetadataClient(object):
    """A class used as a metadata client

    Attributes
    ----------
    component : str
        the extension component
    version : str
        the extension component version
    extension_metadata : dict
        the extension metadata

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
            the extension component
        version : str
            the extension component version
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

        self.use_latest_metadata = kwargs.pop('use_latest_metadata', False)
        self.extension_metadata = self._load_metadata()
        self.component = self._validate_component(component)
        self.version = self._validate_component_version(
            self.component,
            version or self.get_latest_version()
        )

    def _load_metadata(self):
        """Load extension metadata

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
            parsed_url = http_utils.parse_url(EXTENSION_METADATA['URL'])
            try:
                metadata = http_utils.make_request(parsed_url['host'], parsed_url['path'])
            except Exception as err:  # pylint: disable=broad-except
                self.logger.warning('Error downloading metadata file: %s', err)

        # fallback to local metadata file
        if metadata is None:
            local_file = os.path.join(os.path.dirname(__file__), EXTENSION_METADATA['FILE'])
            try:
                with open(local_file) as m_file:
                    metadata = json.loads(m_file.read())
            except Exception as err:  # pylint: disable=broad-except
                raise FileLoadError(err)

        return metadata

    def _validate_component(self, component):
        """Validates the extension component exists in metadata

        Parameters
        ----------
        component : str
            a extension component to check

        Returns
        -------
        str
            the extension component provided if it exists (see Raises)

        Raises
        ------
        Exception
            if the extension component does not exist in metadata
        """

        components = list(self.extension_metadata['components'].keys())
        if not [i for i in components if i == component]:
            raise InvalidComponentError('Valid component must be provided: %s' % (components))
        return component

    def _validate_component_version(self, component, version):
        """Validates the extension component version exists in metadata

        Parameters
        ----------
        component : str
            a extension component to check
        version : str
            a extension component version to check

        Returns
        -------
        str
            the extension component version provided if it exists (see Raises)

        Raises
        ------
        Exception
            if the extension component version does not exist in metadata
        """

        versions = list(self.extension_metadata['components'][component]['versions'].keys())
        if not [i for i in versions if i == version]:
            raise InvalidComponentVersionError(
                'Valid component version must be provided: %s' % (versions)
            )
        return version

    def _get_component_metadata(self):
        """Gets the metadata for a specific component from the extension metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the metadata
        """

        return self.extension_metadata['components'][self.component]

    def _get_version_metadata(self):
        """Gets the metadata for a specific component version from the extension metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the metadata
        """

        return self.extension_metadata['components'][self.component]['versions'][self.version]

    def get_latest_version(self):
        """Gets the latest component version from the extension metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the latest version
        """

        c_v_metadata = self.extension_metadata['components'][self.component]['versions']
        latest = {k: v for (k, v) in c_v_metadata.items() if v['latest']}
        return list(latest.keys())[0]  # we should only have one

    def get_versions_list(self):
        """Lists all the component versions from the extension metadata

        Parameters
        ----------
        None

        Returns
        -------
        list
            a list containing all versions
        """

        return list(self.extension_metadata['components'][self.component]['versions'].keys())

    def get_download_url(self):
        """Gets the component versions download url from extension metadata

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
        """Gets the component versions package name from extension metadata

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
        """Gets the component's package name from extension metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the component's package name, i.e. 'f5-telemetry'
        """

        match = re.search('.+?(?=-[0-9])', self._get_version_metadata()['packageName'])

        return match.group(0)

    def get_component_dependencies(self):
        """Gets the component dependencies

        Parameters
        ----------
        None

        Returns
        -------
        dict
            describes the component dependencies
        """

        return self._get_component_metadata()['componentDependencies']

    def get_endpoints(self):
        """Gets the component endpoints from extension metadata

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing the endpoints
        """

        return self._get_component_metadata()['endpoints']
