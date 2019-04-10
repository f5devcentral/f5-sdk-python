""" Module for BIG-IP toolchain package configuration

    Example(s):

    ## Example: Basic
    from f5cloudsdk.bigip import ManagementClient
    from f5cloudsdk.bigip.toolchain import ToolChainClient

    device = ManagementClient('192.0.2.10', user='admin', password='admin')
    as3 = ToolChainClient(device, 'as3')
    # install AS3 package
    as3.package.install()
    # uninstall AS3 package
    as3.package.uninstall()

"""

import os
import json
import time

import f5cloudsdk.constants as constants
import f5cloudsdk.utils as utils

TOOLCHAIN_METADATA = 'toolchain_metadata.json'
PKG_MGMT_URI = '/mgmt/shared/iapp/package-management-tasks'

class Operation(object):
    """ Toolchain package operation client """
    def __init__(self, client, component):
        self._client = client
        self.component = component
        self.t_metadata = self._load_metadata()

    @staticmethod
    def _load_metadata():
        """ Load toolchain metadata """
        with open(os.path.join(os.path.dirname(__file__), TOOLCHAIN_METADATA)) as m_file:
            metadata = json.loads(m_file.read())
        return metadata

    def _get_latest_version(self):
        """ Get latest version from toolchain metadata """
        c_v_metadata = self.t_metadata['components'][self.component]['versions']
        latest = {k: v for (k, v) in c_v_metadata.items() if v['latest']}
        return list(latest.keys())[0] # we should only have one

    def _get_version_metadata(self, version):
        """ Get specific version metadata from toolchain metadata """
        return self.t_metadata['components'][self.component]['versions'][version]

    def _get_download_url(self, version):
        """ Get download url from toolchain metadata for a specific version """
        v_metadata = self._get_version_metadata(version)
        return v_metadata['downloadUrl']

    def _get_package_name(self, version):
        """ Get package name from toolchain metadata for a specific version """
        v_metadata = self._get_version_metadata(version)
        return v_metadata['packageName']

    def _upload_rpm(self, file_name, **kwargs):
        """ Upload local rpm file to remote BIG-IP """
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
        """ Check RPM task status on remote BIG-IP """
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
        """ Install RPM on remote BIG-IP """
        uri = PKG_MGMT_URI
        body = {
            'operation': 'INSTALL',
            'packageFilePath': package_path
        }
        response = self._client.make_request(uri, method='POST', body=body)

        # now check for task status completion
        self._check_rpm_task_status(response['id'])

    def install(self, **kwargs):
        """ Install toolchain package """
        component = self.component
        version = kwargs.pop('version', self._get_latest_version())

        # download package (rpm) locally, upload to BIG-IP, install on BIG-IP
        download_url = self._get_download_url(version)
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
        """ Uninstall RPM on remote BIG-IP """
        uri = PKG_MGMT_URI
        body = {
            'operation': 'UNINSTALL',
            'packageName': package_name
        }
        response = self._client.make_request(uri, method='POST', body=body)
        # now check for task status completion
        self._check_rpm_task_status(response['id'])

    def uninstall(self, **kwargs):
        """ Uninstall toolchain package """
        component = self.component
        version = kwargs.pop('version', self._get_latest_version())

        # uninstall from BIG-IP
        package_name = self._get_package_name(version)
        self._uninstall_rpm(package_name)
        return {'component': component, 'version': version} # temp

    def _list_rpm(self, package_name):
        """ List RPM on remote BIG-IP """
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

    def is_installed(self, **kwargs):
        """ Check if toolchain package is installed """
        version = kwargs.pop('version', self._get_latest_version())

        # list installed packages, check if this version's package name is installed
        package_name = self._get_package_name(version)
        # list
        response = self._list_rpm(package_name)
        return response
