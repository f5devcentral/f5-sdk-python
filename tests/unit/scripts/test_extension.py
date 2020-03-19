""" Test extension metadata generator module """

# project imports
from f5sdk.scripts.extension.generate_metadata import ExtensionScraperClient
# unittest imports
from ...shared import mock_utils
from ...global_test_imports import pytest

COMPONENTS = ['as3', 'do', 'ts', 'cf'].sort()
MOCK_CONDITIOINS = [
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

@pytest.fixture(name='mocked_requests')
def fixture_mocked_requests(mocker):
    """ Test fixture """

    mock_requests = mocker.patch('requests.request')
    mock_requests.side_effect = mock_utils.create_response(
        {}, conditional=MOCK_CONDITIOINS
    )
    return mock_requests



class TestExtensionMetadataGenerator(object):
    """Test Class: extension generate metadata module """

    @pytest.mark.usefixtures("mocked_requests")
    @staticmethod
    def test_extension_metadata_components():
        """Test: Extension generator generates metadata components

        Assertions
        ----------
        - Metadata file should generate components correctly
        """

        extension_scraper = ExtensionScraperClient()
        extension_metadata = extension_scraper.generate_metadata(write_file=False)

        assert list(extension_metadata['components'].keys()).sort() == COMPONENTS

    @pytest.mark.usefixtures("mocked_requests")
    @staticmethod
    def test_extension_metadata_versions():
        """Test: Extension generator generates metadata component versions

        Exercises both release assets and dist folder for download
        URL and package name discovery

        Assertions
        ----------
        - Metadata file should generate component versions correctly
        """

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

    @staticmethod
    def test_extension_metadata_versions_with_two_artifacts(mocked_requests):
        """Test: Extension generator generates metadata component versions,
        when a single tagged version contains two releases

        Exercises both release assets and dist folder for download
        URL and package name discovery

        Assertions
        ----------
        - Metadata file should generate component versions correctly
        """

        mock_conditions = [
            {
                'type': 'url',
                'value': '/releases/latest',
                'response': {
                    'body': {
                        'tag_name': 'v2.0.0'
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
                                },
                                {
                                    'name': 'pkg-1.0.0.rpm',
                                    'browser_download_url': 'https://site.com/pkg-1.0.0.rpm'
                                }
                            ]
                        }
                    ]
                }
            }
        ]

        mocked_requests.side_effect = mock_utils.create_response(
            {},
            conditional=mock_conditions
        )

        extension_scraper = ExtensionScraperClient()
        extension_metadata = extension_scraper.generate_metadata(write_file=False)

        assert extension_metadata['components']['as3']['versions'] == {
            '1.1.0': {
                'downloadUrl': 'https://site.com/pkg-1.1.0.rpm',
                'packageName': 'pkg-1.1.0',
                'latest': False
            },
            '1.0.0': {
                'downloadUrl': 'https://site.com/pkg-1.0.0.rpm',
                'packageName': 'pkg-1.0.0',
                'latest': False
            }
        }

    @pytest.mark.usefixtures("mocked_requests")
    @staticmethod
    def test_extension_metadata_component_dependencies():
        """Test: Extension generator generates metadata component dependencies

        Assertions
        ----------
        - Metadata file should provide component dependencies for 'as3'
        """

        extension_scraper = ExtensionScraperClient()
        extension_metadata = extension_scraper.generate_metadata(write_file=False)

        deps = list(extension_metadata['components']['as3']['componentDependencies'].keys())
        assert 'f5-service-discovery' in deps
