import time
import github
from functools import lru_cache

GIT_BASE_URL = 'https://github.com/'
GITHUB_API = github.Github()


def rate_limiter(min_interval):
    """
    Limits the interval between times the function can be called
    :param min_interval: seconds between function runs
    """
    def decorate(func):
        last_run_time = [time.time()]

        def rate_limited_function(*args, **kargs):
            left_to_wait = last_run_time[0] + min_interval - time.time()
            time.sleep(max(0., left_to_wait))
            ret = func(*args, **kargs)
            last_run_time[0] = time.time()
            return ret

        return rate_limited_function

    return decorate


@lru_cache
@rate_limiter(2)  # gihub api blocks requests if sent too frequent
def github_get_file(repo_url: str, file_path: str, commit_id=None) -> str:
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
