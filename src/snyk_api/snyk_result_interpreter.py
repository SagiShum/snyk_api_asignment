import json

from typing import Dict, Set, List

from snyk_api.code_utils import CodeLocation, code_location_to_code, is_code_valid
from snyk_api.util_functions import github_get_file


class RunResult:
    """
    Object representing a snyk single run result
    """

    def __init__(self, result_json: Dict) -> None:
        self._json = result_json
        self.locations = {CodeLocation.from_json(location_json) for location_json in result_json['locations']}

        for code_flow in result_json['codeFlows']:
            for thread_flow_json in code_flow['threadFlows']:
                self.locations.update(self.thread_flow_json_to_locations(thread_flow_json))

    def thread_flow_json_to_locations(self, thread_flow_json: Dict) -> List[CodeLocation]:
        """
        parses all code locations from a thread flow json. Merges locations contained by consecutive location.
        """
        flow_locations = []
        for location_json in thread_flow_json['locations']:
            curr_location = CodeLocation.from_json(location_json['location'])
            if flow_locations and flow_locations[-1].is_contained(curr_location):
                flow_locations.pop()
            flow_locations.append(curr_location)
        return flow_locations


class SnykResultInterpreter:
    """
    Object representing a snyk result and analytic functionalities on it
    """

    def __init__(self, repo_url: str, json_file_name: str):
        self.repo_url = repo_url
        self.snyk_json = json.loads(github_get_file(repo_url, json_file_name))
        self._run_results = set()
        self._code_locations = set()

    @property
    def code_locations(self) -> Set[CodeLocation]:
        """
        All locations
        :return:
        """
        if not self._code_locations:
            for run_result in self.run_results:
                self._code_locations.update(run_result.locations)
        return self._code_locations

    @property
    def run_results(self):
        """
        Collection of all results in snyk report runs
        :return:
        """
        if not self._run_results:
            for run in self.snyk_json['runs']:
                for result_json in run['results']:
                    self._run_results.add(RunResult(result_json))
        return self._run_results

    def is_result_of_commit(self, commit_id):
        """
        Validates all code locations pointed out by a SNYK result json in commit_id's version
        """
        for code_location in self.code_locations:
            code_file_content = github_get_file(self.repo_url, code_location.uri, commit_id)
            code = code_location_to_code(code_file_content, code_location)
            if not is_code_valid(code):
                return False
        return True
