import re
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .engine import Engine


def s_float(scanner, token): return float(token)


def s_int(scanner, token): return int(token)


def s_operator(scanner, token): return token


scanner = re.Scanner([
    (r'(\+|-)?\d*\.\d*', s_float),
    (r'(\+|-)?\d+', s_int),
    (r'\S+', s_operator),
    (r'\s+', None),
])


class Parser(object):

    def scan(self, input):
        if isinstance(input, str):
            input = StringIO(input)
        for line in input:
            tokens, remainder = scanner.scan(line)
            for t in tokens:
                yield t

    def process(self, input, engine=None):
        if not engine:
            engine = Engine()
        result = None
        for token in self.scan(input):
            if isinstance(token, float) or isinstance(token, int):
                result = engine.push(token)
            else:
                result = engine.execute(token)
        return result
