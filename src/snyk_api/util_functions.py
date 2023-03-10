import time
from numbers import Real
from typing import Optional


import github
from functools import lru_cache

GIT_BASE_URL = 'https://github.com/'
GITHUB_API = github.Github()


def rate_limiter(min_interval: Real):
    """
    Limits the interval between times the function can be called
    :param min_interval: seconds between function runs
    """
    def decorate(func):
        last_run_time = [time.perf_counter()]  # in a list to pass to inner function by reference and not value

        def rate_limited_function(*args, **kargs):
            left_to_wait = last_run_time[0] + min_interval - time.perf_counter()
            time.sleep(max(0., left_to_wait))
            ret = func(*args, **kargs)
            last_run_time[0] = time.perf_counter()
            return ret

        return rate_limited_function

    return decorate


@lru_cache
@rate_limiter(2)  # gihub api blocks requests if sent too frequent
def github_get_file(repo_url: str, file_path: str, commit_id: Optional[str] = None) -> str:
    commit_id = commit_id or github.GithubObject.NotSet
    repo = GITHUB_API.get_repo(repo_url.lstrip(GIT_BASE_URL))
    try:
        return repo.get_contents(file_path, commit_id).decoded_content.decode()  # get contents returns bytes not str
    except AssertionError as assertion_error:  # thrown when file isn't in repository
        return ''
    except github.GithubException as github_exception:
        if github_exception.args[0] == 404:  # file not found
            return ''
        raise


def is_balanced_parentheses(expression: str) -> bool:
    parentheses_types = {'(': ')', '[': ']'}
    parentheses_queue = list()
    for char in expression:
        if char not in list(parentheses_types.keys()) + list(parentheses_types.values()):
            continue
        if char in parentheses_types:
            parentheses_queue.append(char)
            continue

        if not parentheses_queue or not char == parentheses_types[parentheses_queue[-1]]:
            return False
        parentheses_queue.pop()
    return not parentheses_queue
