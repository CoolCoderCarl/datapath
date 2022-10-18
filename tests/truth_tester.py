import truth_seeker


def test_fetch_info():
    """
    Simple test for fetching func
    :return:
    """
    return isinstance(truth_seeker.fetch_info("test"), dict)


def test_fetch_info_empty():
    """
    Empty query
    :return:
    """
    return isinstance(truth_seeker.fetch_info(""), dict)


