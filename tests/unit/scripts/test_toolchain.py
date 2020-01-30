""" Test toolchain metadata generator module """

# project imports
from f5sdk.scripts.toolchain.generate_metadata import ToolChainScraperClient
# unittest imports
from ...shared import mock_utils


class TestToolChainMetadataGenerator(object):
    """Test Class: toolchain generate metadata module """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.components = ['as3', 'do', 'ts', 'failover'].sort()
        cls.mock_conditions = [
            {
                'type': 'url',
                'value': '/releases/latest',
                'response': {
                    'body': {
                        'tag_name': 'v1.1.0'
                    }
                }
            },
            {
                'type': 'url',
                'value': '/releases',
                'response': {
                    'body': [
                        {
                            'tag_name': 'v1.1.0',
                            'assets': [
                                {
                                    'name': 'pkg-1.1.0.rpm',
                                    'browser_download_url': 'https://site.com/pkg-1.1.0.rpm'
                                }
                            ]
                        },
                        {
                            'tag_name': 'v1.0.0',
                            'assets': []
                        }
                    ]
                }
            },
            {
                'type': 'url',
                'value': '/contents/',
                'response': {
                    'body': [
                        {
                            'name': 'pkg-1.0.0.rpm',
                            'download_url': 'https://site.com/pkg-1.0.0.rpm'
                        }
                    ]
                }
            }
        ]

    def test_toolchain_metadata_components(self, mocker):
        """Test: Toolchain generator generates metadata components

        Assertions
        ----------
        - Metadata file should generate components correctly
        """

        mocker.patch('requests.get').side_effect = mock_utils.create_response(
            {}, conditional=self.mock_conditions)

        toolchain_scraper = ToolChainScraperClient()
        toolchain_metadata = toolchain_scraper.generate_metadata(write_file=False)

        assert list(toolchain_metadata['components'].keys()).sort() == self.components

    def test_toolchain_metadata_versions(self, mocker):
        """Test: Toolchain generator generates metadata component versions

        Exercises both release assets and dist folder for download
        URL and package name discovery

        Assertions
        ----------
        - Metadata file should generate component versions correctly
        """

        mocker.patch('requests.get').side_effect = mock_utils.create_response(
            {}, conditional=self.mock_conditions)

        toolchain_scraper = ToolChainScraperClient()
        toolchain_metadata = toolchain_scraper.generate_metadata(write_file=False)

        assert toolchain_metadata['components']['as3']['versions'] == {
            '1.1.0': {
                'downloadUrl': 'https://site.com/pkg-1.1.0.rpm',
                'packageName': 'pkg-1.1.0',
                'latest': True
            },
            '1.0.0': {
                'downloadUrl': 'https://site.com/pkg-1.0.0.rpm',
                'packageName': 'pkg-1.0.0',
                'latest': False
            }
        }
