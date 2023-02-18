import github
from functools import lru_cache


GIT_BASE_URL = 'https://github.com/'
GITHUB_API = github.Github()


@lru_cache
def github_get_file(repo_url, file_path, commit_id=github.GithubObject.NotSet):
    repo = GITHUB_API.get_repo(repo_url.lstrip(GIT_BASE_URL))
    try:
        return repo.get_contents(file_path, commit_id).decoded_content.decode()  # get contents returns bytes not str
    except AssertionError as error:
        return None
