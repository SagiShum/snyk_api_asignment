import pytest
from snyk_api import is_snyk_output_of_commit


@pytest.fixture
def test_repo_url():
    return 'https://github.com/Kirill89/AltoroJ'


@pytest.fixture
def snyk_report_file_name():
    return 'snyk_report_9290fd29843350f5d4a8828a2a282aa9211f33f1.json'


@pytest.mark.parametrize('commit_id,is_true',
                         [
                             ('9290fd29843350f5d4a8828a2a282aa9211f33f1', True),
                             ('3e05087d8a6c9a53b7e002db0d33f6651a7e691b', False),
                             ('554185a1e68ec8c11dd4982169bf3b5f80afe5b3', False),
                             ('f52ded641d39d22fdf4c5cf16e768ba08c03d727', False)
                         ]
                         )
def test_main_functionality(test_repo_url, commit_id, snyk_report_file_name, is_true):
    assert is_true == is_snyk_output_of_commit(test_repo_url, commit_id, snyk_report_file_name)
