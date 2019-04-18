"""Module for BIG-IP toolchain component package configuration

    Examples
    --------
    Example: Basic
    --------------
    from f5cloudsdk.bigip import ManagementClient
    from f5cloudsdk.bigip.toolchain import ToolChainClient

    device = ManagementClient('192.0.2.10', user='admin', password='admin')
    as3 = ToolChainClient(device, 'as3')
    # install AS3 package
    as3.package.install()

    Example: Uninstall
    --------------
    as3.package.uninstall()

    Example: Check if toolchain component is installed
    --------------
    as3.package.is_installed()
"""

import os
import json
import time

import f5cloudsdk.constants as constants
import f5cloudsdk.utils as utils

PKG_MGMT_URI = '/mgmt/shared/iapp/package-management-tasks'

class Operation(object):
    """A class used as a toolchain package operation client for BIG-IP

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
    is_installed()
        Refer to method documentation
    install()
        Refer to method documentation
    uninstall()
        Refer to method documentation
    """

    def __init__(self, client, component, version, toolchain_metadata):
        """Class initialization

        Parameters
        ----------
        client : object
            the management client object
        component : str
            the component in the toolchain
        version : str
            the component version in the toolchain
        toolchain_metadata : dict
            the toolchain metadata

        Returns
        -------
        None
        """

        # init properties
        self._client = client
        self.component = component
        self.version = version
        self.toolchain_metadata = toolchain_metadata

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

    def _get_download_url(self):
        """Gets the component versions download url from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the download url
        """

        v_metadata = self._get_version_metadata()
        return v_metadata['downloadUrl']

    def _get_package_name(self):
        """Gets the component versions package name from toolchain metadata

        Parameters
        ----------
        None

        Returns
        -------
        str
            a string containing the package name
        """

        v_metadata = self._get_version_metadata()
        return v_metadata['packageName']

    def _upload_rpm(self, file_name, **kwargs):
        """Uploads a local RPM file to a remote device

        Parameters
        ----------
        file_name : str
            the name of the local file to upload
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        delete_file : bool
            flag to delete local file when upload is complete

        Returns
        -------
        None
        """

        delete_file = kwargs.pop('delete_file', True)
        uri = '/mgmt/shared/file-transfer/uploads/%s' % (file_name.split('/')[-1])

        file_object = open(file_name, 'rb')
        max_chunk = 1024 * 1024
        file_size = len(file_object.read())
        file_object.seek(0) # move to start
        start_index = 0
        while True:
            file_slice = file_object.read(max_chunk)
            if not file_slice:
                break

            slice_size = len(file_slice)
            if slice_size < max_chunk:
                end = file_size
            else:
                end = start_index + slice_size

            headers = {
                'Content-Range': '%s-%s/%s' % (start_index, end - 1, file_size),
                'Content-Length': str(end),
                'Content-Type': 'application/octet-stream'
            }
            # send chunk
            self._client.make_request(
                uri,
                method='POST',
                headers=headers,
                body=file_slice,
                body_content_type='raw'
            )
            start_index += slice_size

        if delete_file:
            os.remove(file_name)

    def _check_rpm_task_status(self, task_id):
        """Checks RPM task status on a remote device

        Parameters
        ----------
        task_id : str
            the task id to query

        Returns
        -------
        dict
            a dictionary containing the JSON response
        """

        status_link_uri = '%s/%s' % (PKG_MGMT_URI, task_id)
        sleep_secs = 1
        count = 0
        max_count = 120 # max_count + sleep_secs = 2 mins
        while True:
            response = self._client.make_request(status_link_uri)
            if response['status'] == 'FINISHED':
                break
            elif response['status'] == 'FAILED':
                raise Exception(response['errorMessage'])
            elif count > max_count:
                raise Exception('Max count exceeded')
            time.sleep(sleep_secs)
            count += 1
        return response

    def _install_rpm(self, package_path):
        """Installs RPM on a remote device

        Parameters
        ----------
        package_path : str
            the path to the package on the remote device to install

        Returns
        -------
        None
        """

        uri = PKG_MGMT_URI
        body = {
            'operation': 'INSTALL',
            'packageFilePath': package_path
        }
        response = self._client.make_request(uri, method='POST', body=body)

        # now check for task status completion
        self._check_rpm_task_status(response['id'])

    def install(self):
        """Installs toolchain package component on a remote device

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing component and version: {'component': 'as3', 'version': 'x.x.x'}
        """

        component = self.component
        version = self.version

        # download package (rpm) locally, upload to BIG-IP, install on BIG-IP
        download_url = self._get_download_url()
        download_pkg = download_url.split('/')[-1]
        tmp_file = '%s/%s' % (constants.TMP_DIR, download_pkg)
        # download
        utils.download_to_file(download_url, tmp_file)
        # upload
        self._upload_rpm(tmp_file)
        # install
        tmp_file_bigip_path = '/var/config/rest/downloads/%s' % (download_pkg)
        self._install_rpm(tmp_file_bigip_path)
        return {'component': component, 'version': version} # temp

    def _uninstall_rpm(self, package_name):
        """Uninstalls RPM (LX extension) on a remote device

        Parameters
        ----------
        package_name : str
            the name of the installed package

        Returns
        -------
        None
        """

        uri = PKG_MGMT_URI
        body = {
            'operation': 'UNINSTALL',
            'packageName': package_name
        }
        response = self._client.make_request(uri, method='POST', body=body)
        # now check for task status completion
        self._check_rpm_task_status(response['id'])

    def uninstall(self):
        """Uninstalls toolchain package component on a remote device

        Parameters
        ----------
        None

        Returns
        -------
        dict
            a dictionary containing component and version: {'component': 'as3', 'version': 'x.x.x'}
        """

        component = self.component
        version = self.version

        # uninstall from BIG-IP
        package_name = self._get_package_name()
        self._uninstall_rpm(package_name)
        return {'component': component, 'version': version} # temp

    def _check_rpm_exists(self, package_name):
        """Checks RPM (LX extension) exists on a remote device

        Parameters
        ----------
        package_name : str
            the name of the installed package

        Returns
        -------
        bool
            a boolean based on RPM existence
        """

        uri = PKG_MGMT_URI
        body = {
            'operation': 'QUERY'
        }
        response = self._client.make_request(uri, method='POST', body=body)

        # now check for task status completion
        response = self._check_rpm_task_status(response['id'])
        # check queryResponse for matching package_name
        query_response = response['queryResponse']
        matching_packages = [i for i in query_response if i['packageName'] == package_name]
        return len(matching_packages) == 1

    def is_installed(self):
        """Checks if the toolchain component package is installed on a remote device

        Parameters
        ----------
        None

        Returns
        -------
        bool
            a boolean based on toolchain component package existence
        """

        # list installed packages, check if this version's package name is installed
        package_name = self._get_package_name()
        response = self._check_rpm_exists(package_name)
        return response
