import json

from typing import Dict, Set
from dataclasses import dataclass
from file_getter import github_get_file


@dataclass(eq=True, frozen=True)
class CodeLocation:
    uri: str
    uri_base_id: str
    start_line: int
    end_line: int
    start_column: int
    end_column: int

    @classmethod
    def from_json(cls, location_json):
        return cls(
            uri=location_json['physicalLocation']['artifactLocation']['uri'],
            uri_base_id=location_json['physicalLocation']['artifactLocation']['uriBaseId'],
            start_line=location_json['physicalLocation']['region']['startLine'],
            end_line=location_json['physicalLocation']['region']['endLine'],
            start_column=location_json['physicalLocation']['region']['startColumn'],
            end_column=location_json['physicalLocation']['region']['endColumn']
        )


class RunResult:
    def __init__(self, result_json: Dict) -> None:
        self._json = result_json
        self.locations = {CodeLocation.from_json(location_json) for location_json in result_json['locations']}
        for code_flow in result_json['codeFlows']:
            for thread_flow in code_flow['threadFlows']:
                for location_json in thread_flow['locations']:
                    self.locations.add(CodeLocation.from_json(location_json['location']))


class SnykResultInterpreter:
    def __init__(self, repo_url, json_file_name):
        self.repo_url = repo_url
        self.snyk_json = json.loads(github_get_file(repo_url, json_file_name))

    @property
    def code_locations(self) -> Set[CodeLocation]:
        file_paths = set()
        for run in self.snyk_json['runs']:
            for result_json in run['results']:
                file_paths.update(RunResult(result_json).locations)
        return file_paths

    def _code_location_to_code(self, code_file_content: str, location: CodeLocation) -> str:
        code_lines = code_file_content.splitlines()[location.start_line+1:location.end_line+2]
        if not code_lines:
            return ''

        code_lines[0] = code_lines[0][location.start_column:]
        code_lines[-1] = code_lines[-1][:location.end_column+2]
        return '\n'.join(code_lines)

    def _validate_code_location(self, location: CodeLocation, code: str) -> bool:
        if code is None:
            return False
        return True

    def is_result_of_commit(self, commit_id):
        for code_location in self.code_locations:
            code_file_content = github_get_file(self.repo_url, code_location.uri, commit_id)
            code = self._code_location_to_code(code_file_content, code_location)
            if not self._validate_code_location(code_location, code):
                return False
        return True
