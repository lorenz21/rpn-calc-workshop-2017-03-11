"""Parsing engine"""

import re
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .engine import Engine


def s_float(scanner, token):
    """return token as a float"""
    return float(token)


def s_int(scanner, token):
    """return token as an integer"""
    return int(token)


def s_operator(scanner, token):
    """return token as an operation name"""
    return token


_scanner = re.Scanner([
    (r'(\+|-)?\d*\.\d*', s_float),
    (r'(\+|-)?\d+', s_int),
    (r'\S+', s_operator),
    (r'\s+', None),
])


class Parser(object):
    """Input stream parser/tokenizer and processor"""

    def scan(self, stream):
        """scan input stream and return token generator"""
        if isinstance(stream, str):
            stream = StringIO(stream)
        for line in stream:
            tokens, remainder = _scanner.scan(line)
            for t in tokens:
                yield t

    def process(self, stream, engine=None):
        """process all tokens on input stream against calculator engine"""
        if not engine:
            engine = Engine()
        result = None
        for token in self.scan(stream):
            if isinstance(token, float) or isinstance(token, int):
                result = engine.push(token)
            else:
                result = engine.execute(token)
        return result
