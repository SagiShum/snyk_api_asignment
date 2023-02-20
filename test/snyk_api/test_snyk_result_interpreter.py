import pytest
from snyk_api.snyk_result_interpreter import CodeLocation, RunResult
from test.snyk_api.test_jsons import test_thread_flow, test_thread_flow_locations, test_thread_flow_merge_locations, \
    test_thread_flow_merge


def test_code_location_equality():
    location_1 = CodeLocation('a', 'b', 1, 2, 3, 4)
    location_2 = CodeLocation('a', 'b', 1, 2, 3, 4)
    assert location_1 == location_2


@pytest.mark.parametrize(
    "thread_flow_json, code_location_set",
    [
        (test_thread_flow, test_thread_flow_locations),
        (test_thread_flow_merge, test_thread_flow_merge_locations)
    ]
)
def test_run_result_location_parsing(thread_flow_json, code_location_set):
    result_json = dict(locations=[], codeFlows=[dict(threadFlows=[thread_flow_json])])
    run_result = RunResult(result_json)
    assert run_result.locations == code_location_set
