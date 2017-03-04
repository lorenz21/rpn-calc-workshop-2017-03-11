"""Package-wide errors"""


class DuplicateOperationError(Exception):
    """operation has already been registered with given name"""
    pass


class InvalidOperationSignatureError(Exception):
    """operation does not have the required signature"""
    pass


class InvalidValueTypeError(Exception):
    """value cannot be used in operand stack"""
    pass
