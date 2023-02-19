import github
from functools import lru_cache


GIT_BASE_URL = 'https://github.com/'
GITHUB_API = github.Github()


@lru_cache
def github_get_file(repo_url: str, file_path: str, commit_id=None) -> str:
    commit_id = commit_id or github.GithubObject.NotSet
    repo = GITHUB_API.get_repo(repo_url.lstrip(GIT_BASE_URL))
    try:
        return repo.get_contents(file_path, commit_id).decoded_content.decode()  # get contents returns bytes not str
    except AssertionError as error:
        return ''


def is_balanced_parentheses(text):
    count = 0
    for char in text:
        if char == "(" or char == "{" or char == "[":
            count += 1
        elif char == ")" or char == "}" or char == "]":
            count -= 1
        if count < 0:
            return False
    return count == 0


def _validate_code(code: str) -> bool:
    """
    Runs simple code heuristics to validate marked code makes sense
    :param code:
    :return:
    """
    if len(code) == 0:
        return False
    if not is_balanced_parentheses(code):
        return False
    return True
