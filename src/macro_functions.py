from .snyk_result_interpreter import SnykResultInterpreter


def is_snyk_output_of_commit(repo_url: str, commit_id: str, snyk_output_file_path: str) -> bool:
    """
    Macro function that returns whether a snyk output matches the repo's code in commit_id
    :param repo_url: Github repo URL leading with https://gibhub.com
    :param snyk_output_file_path: The path of the snyk output file within the repo
    :param commit_id: commit id in the repo
    """
    interpreter = SnykResultInterpreter(repo_url, snyk_output_file_path)
    return interpreter.is_result_of_commit(commit_id)