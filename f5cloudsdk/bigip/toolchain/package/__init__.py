""" Module for BIG-IP toolchain package configuration """

import os
import json
import requests

import f5cloudsdk.constants as constants

class Operation():
    """ Toolchain package operation client """
    def __init__(self, client, component):
        self.client = client
        self.component = component
        self.t_metadata = self._load_metadata()

    @staticmethod
    def _load_metadata():
        """ Load toolchain metadata """
        with open(os.path.join(os.path.dirname(__file__), 't_metadata.json')) as m_file:
            metadata = json.loads(m_file.read())
        return metadata

    def _get_latest_version(self):
        """ Get latest version from toolchain metadata """
        c_v_metadata = self.t_metadata['components'][self.component]['versions']
        latest = {k: v for (k, v) in c_v_metadata.items() if v['latest']}

        return list(latest.keys())[0] # we should only have one

    def _get_download_url(self, version):
        """ Get download url from toolchain metadata for a specific version """
        return self.t_metadata['components'][self.component]['versions'][version]['downloadUrl']

    @staticmethod
    def download_to_file(url, file_name):
        """ Download to file (using a stream) """
        response = requests.get(url, stream=True)
        with open(file_name, 'wb+') as file_object:
            for chunk in response.iter_content(chunk_size=1024):
                # filter out keep-alive new lines
                if chunk:
                    file_object.write(chunk)

    def _copy_rpm(self, file_name, **kwargs):
        """ Copy local rpm file to remote BIG-IP """
        delete_file = kwargs.pop('delete_file', True)
        url = '/mgmt/shared/file-transfer/uploads/%s' % (file_name.split('/')[-1])

        file_object = open(file_name, 'rb')
        max_chunk = 1024 * 100
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
                'Content-Type': 'application/octet-stream'
            }
            # send chunk
            self.client.make_request(
                url,
                method='POST',
                headers=headers,
                body=file_slice,
                body_content_type='raw'
            )
            # increment index
            start_index += slice_size

        if delete_file:
            os.remove(file_name)

    def _install_rpm(self, package_path):
        """ Install RPM on remote BIG-IP """
        url = '/mgmt/shared/iapp/package-management-tasks'
        body = {
            'operation': 'INSTALL',
            'packageFilePath': package_path
        }
        self.client.make_request(url, method='POST', body=body)

    def install(self, **kwargs):
        """ Install toolchain package """
        component = self.component
        version = kwargs.pop('version', 'latest')

        if version == 'latest':
            version = self._get_latest_version()

        download_url = self._get_download_url(version)
        download_pkg = download_url.split('/')[-1]
        tmp_file = '%s/%s' % (constants.TMP_DIR, download_pkg)
        # download toolchain component package (rpm)
        self.download_to_file(download_url, tmp_file)
        # copy rpm to BIG-IP
        self._copy_rpm(tmp_file)
        # install rpm on BIG-IP
        tmp_file_bigip_path = '/var/config/rest/downloads/%s' % (download_pkg)
        self._install_rpm(tmp_file_bigip_path)
        # TODO: query RPM task status via self link in response

        return {'component': component, 'version': version, 'download_url': download_url} # temp
