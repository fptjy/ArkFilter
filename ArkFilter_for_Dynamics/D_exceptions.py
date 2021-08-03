"""
Exceptions module
"""


class D_ArkFilterFullException(Exception):
    """
    Exception raised when filter is full.
    """
    pass

class D_ArkFilter_cannot_relocate_Exception(Exception):
    """
    Exception raised when the number of re-locate operations has reached the threshold .
    """
    pass
