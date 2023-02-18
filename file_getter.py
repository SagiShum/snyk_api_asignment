from github import Github


GIT_BASE_URL = 'https://github.com/'
GITHUB_API = Github()


def github_get_file(repo_url, file_name):
    repo = GITHUB_API.get_repo(repo_url.lstrip(GIT_BASE_URL))
    return repo.get_contents(file_name).decoded_content
