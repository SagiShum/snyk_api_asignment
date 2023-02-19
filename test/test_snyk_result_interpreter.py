from src.snyk_result_interpreter import CodeLocation


def test_code_location_equality():
    location_1 = CodeLocation('a', 'b', 1, 2, 3, 4)
    location_2 = CodeLocation('a', 'b', 1, 2, 3, 4)
    assert location_1 == location_2
