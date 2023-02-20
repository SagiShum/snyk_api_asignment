from __future__ import annotations
import dataclasses

from typing import Dict
from snyk_api.util_functions import is_balanced_parentheses


@dataclasses.dataclass(eq=True, frozen=True)
class CodeLocation:
    """
    Dataclass object representing a chunk of code within a project
    """
    uri: str
    uri_base_id: str
    start_line: int
    end_line: int
    start_column: int
    end_column: int

    @classmethod
    def from_json(cls, location_json: Dict) -> CodeLocation:
        return cls(
            uri=location_json['physicalLocation']['artifactLocation']['uri'],
            uri_base_id=location_json['physicalLocation']['artifactLocation']['uriBaseId'],
            start_line=location_json['physicalLocation']['region']['startLine'] - 1,
            end_line=location_json['physicalLocation']['region']['endLine'] - 1,
            start_column=location_json['physicalLocation']['region']['startColumn'] - 1,
            end_column=location_json['physicalLocation']['region']['endColumn'] - 1
        )

    def is_contained(self, location: CodeLocation) -> bool:
        """
        :param location: other CodeLocation object
        :return: if other location starts at the same spot as self and is a larger code area
        """
        is_same_start = dataclasses.replace(location, end_column=self.end_column, end_line=self.end_line) == self
        return is_same_start and (location.end_line > self.end_line or location.end_column >= self.end_column)


def is_code_valid(code: str) -> bool:
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


def code_location_to_code(code_file_content: str, location: CodeLocation) -> str:
    """
    Returns the code within file content confined by a code location object
    """
    code_lines = code_file_content.splitlines()[location.start_line:location.end_line + 1]
    if not code_lines:
        return ''
    if len(code_lines[0]) < location.start_column or len(code_lines[-1]) < location.end_column:
        return ''

    code_lines[-1] = code_lines[-1][:location.end_column]
    code_lines[0] = code_lines[0][location.start_column:]
    return '\n'.join(code_lines)
