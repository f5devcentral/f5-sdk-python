"""Generate toolchain metadata file

Example output:
{
    "components": {
        "as3": {
            "endpoints": {
                "configure": {
                    "uri": "",
                    "methods": ["GET"]
                }
            },
            "versions": {
                "1.0.0": {
                    "downloadUrl": "",
                    "packageName": "",
                    "latest": true
                }
            }
        }
    }
}
"""

import os
import json
import requests

import f5sdk.constants as constants
from f5sdk.exceptions import FileLoadError

EXTENSION_INFO = 'extension_info.json'
GITHUB_ENDPOINT = 'https://github.com'
GITHUB_API_ENDPOINT = 'https://api.github.com'


def log(message):
    """Logger

    Parameters
    ----------
    message : str
        the message to log

    Returns
    -------
    None
    """

    print(message)


class ToolChainScraperClient():
    """Toolchain scraper client

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    def __init__(self):
        self.output_file = os.path.join(os.getcwd(), 'metadata.json')

        try:
            with open(os.path.join(os.path.dirname(__file__), EXTENSION_INFO)) as m_file:
                self.toolchain_components = json.loads(m_file.read())
        except Exception as err:  # pylint: disable=broad-except
            raise FileLoadError(err)

    @staticmethod
    def _normalize_tag_name(tag):
        """Normalize tag name into 'x.x.x'

        Parameters
        ----------
        tag : str
            tag name

        Returns
        -------
        str
            the normalized tag name
        """

        if tag[0] == 'v':
            tag = tag[1:]

        return tag

    def _get_download_url(self, assets, tag_name):
        """Get download URL out of api response

        Should look similar to the following:
        - f5-declarative-onboarding-1.1.0-1.noarch.rpm

        Note: Some assets may have multiple RPM versions
        associated with a release, filter which RPM to use
        based on matching tag name

        Parameters
        ----------
        items : array
            release assets or repository contents

        Returns
        -------
        str
            the resolved download URL
        """

        tag_name = self._normalize_tag_name(tag_name)

        rpms = [i for i in assets if i['name'].find(".rpm") != -1
                and i['name'].find(".sha") == -1
                and i['name'].find(tag_name) != -1]

        # check for length > 1, if this fails the logic needs to be reviewed
        if len(rpms) > 1:
            raise Exception('RPM count is more than expected: {}'.format(rpms))
        if len(rpms) == 1:
            rpm_info = rpms[0]
            if 'download_url' in rpm_info:
                return rpm_info['download_url']
            if 'browser_download_url' in rpm_info:
                return rpm_info['browser_download_url']

        return None

    @staticmethod
    def _get_repo_contents(repository, tag):
        """Get repository contents (from dist folder)

        Parameters
        ----------
        repository : str
            repository name
        tag_name : str
            repository tag

        Returns
        -------
        array
            the repository contents
        """

        response = requests.get(
            '{}/repos/{}/contents/{}?ref={}'.format(
                GITHUB_API_ENDPOINT,
                repository,
                'dist',
                tag
            )
        )
        # check if status code is not '200'
        if response.status_code == constants.HTTP_STATUS_CODE['OK']:
            return response.json()
        return None

    def _resolve_artifact_info(self, release, repo_info):
        """Resolve artifact information, such as download URL and package name

        Attempt to resolve in the following order:
        - Github releases artifact
        - Inside source code 'dist' folder

        Parameters
        ----------
        release : dict
            release information
        repo_info : dict
            repository information

        Returns
        -------
        dict
            the resolved artifact information
            {
                'download_url': '',
                'package_name': '',
                'latest': True
            }
        """

        ret = {
            'download_url': None,
            'package_name': None,
            'latest': False
        }

        # search for the download URL information in the following order
        # - release assets
        # - 'dist' folder
        assets_url = self._get_download_url(release['assets'], release['tag_name'])
        if assets_url is not None:
            ret['download_url'] = assets_url
        else:
            contents_url = self._get_download_url(
                self._get_repo_contents(repo_info['repository'], release['tag_name']),
                release['tag_name']
            )
            if contents_url is not None:
                ret['download_url'] = contents_url

        # resolve package name from download url
        if ret['download_url'] is not None:
            ret['package_name'] = ret['download_url'].split('/')[-1].split('.rpm')[0]

        return ret

    def _get_component_versions(self, component_info):
        """Get component versions

        Parameters
        ----------
        None

        Returns
        -------
        dict
            the component versions
            {
                '1.0.0': {
                    'downloadUrl': '',
                    'packageName': '',
                    'latest': True
                }
            }
        """

        ret = {}

        response = requests.get(
            '{}/repos/{}/releases'.format(GITHUB_API_ENDPOINT, component_info['repository'])
        )
        response.raise_for_status()  # check for errors, such as API rate limits

        latest_release_tag_name = requests.get(
            '{}/repos/{}/releases/latest'.format(GITHUB_API_ENDPOINT, component_info['repository'])
        ).json()['tag_name']

        for release in response.json():
            release_info = self._resolve_artifact_info(release, component_info)
            ret[self._normalize_tag_name(release['tag_name'])] = {
                'downloadUrl': release_info['download_url'],
                'packageName': release_info['package_name'],
                'latest': latest_release_tag_name == release['tag_name']
            }

        return ret

    def generate_metadata(self, **kwargs):
        """Generate metadata and save to output file

        Parameters
        ----------
        **kwargs :
            optional keyword arguments

        Keyword Arguments
        -----------------
        write_file : bool
            specify whether file should be written to disk

        Returns
        -------
        dict
            generated metadata
        """

        write_file = kwargs.pop('write_file', True)

        metadata = {
            'components': {}
        }

        for component, info in self.toolchain_components.items():
            metadata['components'][component] = {
                'endpoints': info['endpoints'],
                'versions': self._get_component_versions(info)
            }

        if write_file:
            log('Writing metadata file to {}'.format(self.output_file))
            with open(self.output_file, 'w+') as output_file:
                output_file.write(json.dumps(metadata, indent=4))

        return metadata


if __name__ == "__main__":
    TCS_CLIENT = ToolChainScraperClient()
    TCS_CLIENT.generate_metadata()
