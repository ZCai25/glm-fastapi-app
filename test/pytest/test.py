import pytest

@pytest.mark.parametrize("test_input", [1, 2, 3])
def test_example(test_input):
    print(f"Testing with input: {test_input}")
    assert test_input > 0