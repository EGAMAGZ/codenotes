def status_text(status: int) -> str:
    """ Functions that returns the status in text

    Parameters
    ----------
    status : int
        Int status of the task
    """
    if status == 0:
        return 'Incomplete'
    elif status == 1:
        return 'In Process'
    elif status == 2:
        return 'Finished'
