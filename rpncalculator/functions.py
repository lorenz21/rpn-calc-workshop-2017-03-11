"""Built-in function library"""

import sys


def register(operator_name):
    """decorator to mark functions for auto-registration"""
    def decorator(functor):
        """perform the marking for auto-registration"""
        functor.is_registerable = True
        functor.operator_name = operator_name
        return functor
    return decorator


def register_all(engine):
    """iterate over all members of this module and register all functors with
    'register' attribute"""
    for name, val in sys.modules[__name__].__dict__.items():  # noqa
        if hasattr(val, 'is_registerable'):
            engine.register(val.operator_name, val)


@register('+')
def add(engine):
    """add the top two numbers on the stack"""
    engine.push(engine.pop() + engine.pop())


@register('/')
def divide(engine):
    """floating-point divide stack[-2] by stack[-1]"""
    dividend = engine.pop()
    divisor = engine.pop()
    engine.push(1. * divisor / dividend)


@register('in2cm')
def in2cm(engine):
    """multiply stack[-1] by 2.54"""
    inches = engine.pop()
    engine.push(inches * 2.54)


@register('*')
def multiplication(engine):
    """add the top two numbers on the stack"""
    engine.push(engine.pop() * engine.pop())


@register('neg')
def negate(engine):
    """negates the top number on the stack"""
    engine.push(-engine.pop())
