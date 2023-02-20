from time import sleep

import github
from functools import lru_cache


GIT_BASE_URL = 'https://github.com/'
GITHUB_API = github.Github()


@lru_cache
def github_get_file(repo_url: str, file_path: str, commit_id=None) -> str:
    sleep(2)  # github api blocks requests if too frequent
    commit_id = commit_id or github.GithubObject.NotSet
    repo = GITHUB_API.get_repo(repo_url.lstrip(GIT_BASE_URL))
    try:
        return repo.get_contents(file_path, commit_id).decoded_content.decode()  # get contents returns bytes not str
    except AssertionError as assertion_error:
        return ''
    except github.GithubException as github_exception:
        if github_exception.args[0] == 404:
            return ''
        raise


def is_balanced_parentheses(expression):
    parentheses_openers = ['(', '[']
    parentheses_closers = [')', ']']
    count = 0
    for char in expression:
        if char in parentheses_openers:
            count += 1
        elif char in parentheses_closers:
            count -= 1
        if count < 0:
            return False
    return count == 0
