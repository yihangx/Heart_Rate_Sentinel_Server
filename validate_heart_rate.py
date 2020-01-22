def validate_heart_rate(age, heart_rate):
    """ Validate the average of heart rate, and return
    the patient's status.
    Args:
        age(int): patient'age
        heart_rate(int): measured heart rates
    Returns:
        status(string): average heart rate
    """
    status = ""
    if age < 1:
        tachycardia_threshold = -1
    if age in range(1, 3):
        tachycardia_threshold = 151
    if age in range(3, 5):
        tachycardia_threshold = 137
    if age in range(5, 8):
        tachycardia_threshold = 133
    if age in range(8, 12):
        tachycardia_threshold = 130
    if age in range(12, 16):
        tachycardia_threshold = 119
    if age > 15:
        tachycardia_threshold = 100
    if tachycardia_threshold != -1:
        if heart_rate >= tachycardia_threshold:
            status = "tachycardia"
        else:
            status = "not tachycardia"
    return status
