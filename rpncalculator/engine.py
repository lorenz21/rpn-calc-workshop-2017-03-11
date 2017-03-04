"""Calculation engine"""

try:
    from inspect import signature as funcsignature
except ImportError:
    from funcsigs import signature as funcsignature

from .errors import DuplicateOperationError
from .errors import InvalidOperationSignatureError
from .errors import InvalidValueTypeError
from .functions import register_all


def noop(engine):  # pylint: disable=W0613
    """No-Op (do nothing) operator"""
    return


class Engine(object):
    """Calculation engine"""

    def __init__(self, auto_register=True):
        self._stack = []
        self._operations = {'noop': noop}
        if auto_register:
            register_all(self)

    def pop(self):
        """remove one value from the stack and return it"""
        if len(self._stack) == 0:
            return None
        return self._stack.pop()

    def push(self, value):
        """push a value to the stack, value must be of a numeric type"""
        if not isinstance(value, int) and not isinstance(value, float):
            raise InvalidValueTypeError()
        self._stack.append(value)
        return value

    def execute(self, operation):
        """execute the named operation on the current stack"""
        self._operations[operation](engine=self)
        return self._stack[-1]

    def register(self, operation, function):
        """register an operation with the provided unique name"""
        signature = funcsignature(function)
        if (
                len(signature.parameters) != 1
                or 'engine' not in signature.parameters
        ):
            raise InvalidOperationSignatureError()
        if operation in self._operations:
            raise DuplicateOperationError()
        self._operations[operation] = function
