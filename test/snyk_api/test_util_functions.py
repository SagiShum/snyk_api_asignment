import pytest
from pytest import fixture

from snyk_api.code_utils import is_code_valid
from snyk_api.util_functions import github_get_file, is_balanced_parentheses


@fixture
def test_repo_url():
    return 'https://github.com/Kirill89/AltoroJ'


@pytest.mark.parametrize('file_name,is_valid', [('abcdefg', False), ('.gitignore', True)])
def test_github_get_file(test_repo_url, file_name, is_valid):
    file_content = github_get_file(test_repo_url, file_name)
    assert isinstance(file_content, str) and bool(file_content) == is_valid


@pytest.mark.parametrize('expression,is_valid', [
    ('([()])', True), ('', True), ('(()[]())', True), ('[()]{}', True),
    ('([()]', False), (')', False), ('()][]', False)
]
                         )
def test_is_balanced_parentheses(expression, is_valid):
    assert is_balanced_parentheses(expression) == is_valid


@pytest.mark.parametrize('code,is_valid', [
    ('module.function', True),
    ('equest.getParameter(', False),
    ('', False),
    ('module.function(parameter)', True)
]
                         )
def test_validate_code_valid(code, is_valid):
    assert is_code_valid(code) == is_valid
