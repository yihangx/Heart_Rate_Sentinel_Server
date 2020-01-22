import pytest
from validate_heart_rate import validate_heart_rate


@pytest.mark.parametrize("test_input, expected", [
    ([26, 152], "tachycardia"),
    ([32, 78], "not tachycardia"),
    ([14, 118], "not tachycardia"),
])
def test_validate_heart_rate(test_input, expected):
    """ Validate the average of heart rate, and return
    the patient's status.
    Args:
        test_input(list): patient'heart rate
        expected(str): patient's status
    Returns:
        None
    """
    assert(validate_heart_rate(test_input[0], test_input[1]) == expected)
