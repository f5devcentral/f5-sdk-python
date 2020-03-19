"""Generate extension metadata file

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
import re
import json

from f5sdk.exceptions import FileLoadError
from f5sdk.utils import http_utils

EXTENSION_INFO = 'extension_info.json'
GITHUB_API_ENDPOINT = 'api.github.com'
VERSION_REGEX = '[0-9]+.[0-9]+.[0-9]+'


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


class ExtensionScraperClient():
    """Extension scraper client

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
                self.extension_components = json.loads(m_file.read())
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

    @staticmethod
    def _get_download_url(asset):
        """Get download URL from asset

        Parameters
        ----------
        asset : dict
            release asset or repository contents

        Returns
        -------
        str
            artifact download URL
        """

        if 'download_url' in asset:
            return asset['download_url']
        if 'browser_download_url' in asset:
            return asset['browser_download_url']
        return ''

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

        return http_utils.make_request(
            GITHUB_API_ENDPOINT,
            '/repos/{}/contents/{}?ref={}'.format(repository, 'dist', tag)
        )

    def _parse_artifacts(self, assets, tag_name):
        """Parse artifacts

        Note: Some assets may have multiple RPM versions
        associated with a release, add an artifact for each asset
        and set an 'is_primary' flag based on tag name

        Parameters
        ----------
        assets : array
            release assets or repository contents

        Returns
        -------
        list
            artifacts information:
            [
                {
                    'url': '',
                    'is_primary': True
                }
            ]
        """

        tag_name = self._normalize_tag_name(tag_name)
        rpms = [i for i in assets if i['name'].find(".rpm") != -1
                and i['name'].find(".sha") == -1]

        artifacts = []
        for rpm in rpms:
            url = self._get_download_url(rpm)
            artifacts.append({
                'url': url,
                'is_primary': url.split('/')[:1][0].find(tag_name) != -1
            })
        return artifacts

    def _resolve_artifacts_info(self, tag_name, assets, repo_info):
        """Resolve information about artifacts, such as download URL and package name

        Attempt to resolve in the following order:
        - Github releases artifacts
        - Inside source code 'dist' folder

        Parameters
        ----------
        tag_name : str
            tag name of the release
        assets : list
            assets in the release

        Returns
        -------
        list
            the resolved artifacts information
            [{
                'download_url': '',
                'package_name': ''
            }]
        """

        # search for the artifacts information in the following order
        # - release assets
        # - 'dist' folder
        artifacts_info = self._parse_artifacts(assets, tag_name)
        if not artifacts_info: # not in release assets, try 'dist' folder
            artifacts_info = self._parse_artifacts(
                self._get_repo_contents(repo_info['repository'], tag_name),
                tag_name
            )

        if not artifacts_info:
            raise Exception('Unable to resolve artifacts info: {}'.format(artifacts_info))

        ret = []
        for artifact in artifacts_info:
            ret.append({
                'download_url': artifact['url'],
                'package_name': artifact['url'].split('/')[-1].split('.rpm')[0],
                'is_primary': artifact['is_primary']
            })
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

        releases = http_utils.make_request(
            GITHUB_API_ENDPOINT,
            '/repos/{}/releases'.format(component_info['repository'])
        )
        latest_release_tag_name = http_utils.make_request(
            GITHUB_API_ENDPOINT,
            '/repos/{}/releases/latest'.format(component_info['repository'])
        )['tag_name']

        ret = {}
        for release in releases:
            release_artifacts = self._resolve_artifacts_info(
                release['tag_name'],
                release['assets'],
                component_info
            )
            for artifact in release_artifacts:
                # - "if primary" use the release version as the key
                # - "if not primary" parse the version from the artifact package name
                if artifact['is_primary']:
                    release_version = self._normalize_tag_name(release['tag_name'])
                else:
                    release_version = re.search(VERSION_REGEX, artifact['package_name']).group(0)

                ret[release_version] = {
                    'downloadUrl': artifact['download_url'],
                    'packageName': artifact['package_name'],
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

        for component, info in self.extension_components.items():
            metadata['components'][component] = {
                'endpoints': info['endpoints'],
                'versions': self._get_component_versions(info),
                'componentDependencies': info['componentDependencies']
            }

        if write_file:
            log('Writing metadata file to {}'.format(self.output_file))
            with open(self.output_file, 'w+') as output_file:
                output_file.write(json.dumps(metadata, indent=4))

        return metadata


if __name__ == "__main__":
    TCS_CLIENT = ExtensionScraperClient()
    TCS_CLIENT.generate_metadata()
