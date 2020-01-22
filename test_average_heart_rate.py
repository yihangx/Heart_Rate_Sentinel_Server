import pytest
from average_heart_rate import average_heart_rate


@pytest.mark.parametrize("test_input, expected", [
    ([78, 80], 79),
    ([123, 125], 124)
])
def test_average_heart_rate(test_input, expected):
        """ Test average_heart_rate function.
    Args:
        test_input(list): assert result
        expected (int) : expected result
    Returns:
        None
    """
        assert(average_heart_rate(test_input) == expected)
