""" Test extension metadata generator module """

# project imports
from f5sdk.scripts.extension.generate_metadata import ExtensionScraperClient
# unittest imports
from ...shared import mock_utils


class TestExtensionMetadataGenerator(object):
    """Test Class: extension generate metadata module """

    @classmethod
    def setup_class(cls):
        """" Setup func """
        cls.components = ['as3', 'do', 'ts', 'cf'].sort()
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

    def test_extension_metadata_components(self, mocker):
        """Test: Extension generator generates metadata components

        Assertions
        ----------
        - Metadata file should generate components correctly
        """

        mocker.patch('requests.get').side_effect = mock_utils.create_response(
            {}, conditional=self.mock_conditions)

        extension_scraper = ExtensionScraperClient()
        extension_metadata = extension_scraper.generate_metadata(write_file=False)

        assert list(extension_metadata['components'].keys()).sort() == self.components

    def test_extension_metadata_versions(self, mocker):
        """Test: Extension generator generates metadata component versions

        Exercises both release assets and dist folder for download
        URL and package name discovery

        Assertions
        ----------
        - Metadata file should generate component versions correctly
        """

        mocker.patch('requests.get').side_effect = mock_utils.create_response(
            {}, conditional=self.mock_conditions)

        extension_scraper = ExtensionScraperClient()
        extension_metadata = extension_scraper.generate_metadata(write_file=False)

        assert extension_metadata['components']['as3']['versions'] == {
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

    def test_extension_metadata_component_dependencies(self, mocker):
        """Test: Extension generator generates metadata component dependencies

        Assertions
        ----------
        - Metadata file should provide component dependencies for 'as3'
        """

        mocker.patch('requests.get').side_effect = mock_utils.create_response(
            {}, conditional=self.mock_conditions)

        extension_scraper = ExtensionScraperClient()
        extension_metadata = extension_scraper.generate_metadata(write_file=False)

        deps = list(extension_metadata['components']['as3']['componentDependencies'].keys())
        assert 'f5-service-discovery' in deps
