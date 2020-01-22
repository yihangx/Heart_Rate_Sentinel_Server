def average_heart_rate(heart_rate_list):
    """ Caculate the average of heart rate.
    Args:
        heart_rate_list(list): list contains the measured heart rates
    Returns:
        hr(int): average heart rate
    """
    import numpy as np
    hr = int(np.sum(heart_rate_list) / len(heart_rate_list))
    return hr
