import unittest

import collections
import mock
import os
import types

import rpncalculator


test_input_single_line = '1 +2 -3 4.0 +5.1 -6.2 a'
test_input_multi_line = """1
+2
 -3 4.0
      +5.1
-6.2 a"""
expected_tokenization = [1, 2, -3, 4.0, 5.1, -6.2, 'a']


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.parser = rpncalculator.Parser()

    def test_parser_tokenizer_returns_generator(self):
        tokenizer = self.parser.scan('')
        self.assertIsInstance(tokenizer, collections.Iterable)
        self.assertIsInstance(tokenizer, types.GeneratorType)

    def test_parser_tokenizes_input_on_whitespace(self):
        self.assertEqual(
            list(self.parser.scan(test_input_single_line)),
            expected_tokenization
            )

    def test_parser_tokenizes_multi_line_input(self):
        self.assertEqual(
            list(self.parser.scan(test_input_multi_line)),
            expected_tokenization
            )

    def test_parser_tokenizes_file_input(self):
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'file_for_parsing.txt'
            )
        with open(path) as infile:
            self.assertEqual(
                list(self.parser.scan(infile)),
                expected_tokenization
                )


class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.parser = rpncalculator.Parser()
        self.engine = rpncalculator.Engine()
        self.engine.push = mock.MagicMock(return_value=None)
        self.engine.execute = mock.MagicMock(return_value=0)

    def test_processor_calls_push_with_int_value(self):
        self.parser.scan = mock.MagicMock(return_value=[1])
        self.parser.process(None, self.engine)
        self.engine.push.assert_called_once()
        self.engine.execute.assert_not_called()

    def test_processor_calls_push_with_float_value(self):
        self.parser.scan = mock.MagicMock(return_value=[1.])
        self.parser.process(None, self.engine)
        self.engine.push.assert_called_once()
        self.engine.execute.assert_not_called()

    def test_processor_calls_execute_with_string_value(self):
        self.parser.scan = mock.MagicMock(return_value=['x'])
        self.parser.process(None, self.engine)
        self.engine.push.assert_not_called()
        self.engine.execute.assert_called_once()

    def test_processor_engine_is_optional(self):
        self.parser.scan = mock.MagicMock(return_value=[1.])
        self.parser.process(None)

    def test_processor_returns_value_if_push_is_last_action(self):
        self.assertEqual(self.parser.process('123'), 123)

    def test_processor_returns_value_if_execute_is_last_action(self):
        self.assertEqual(self.parser.process('123 noop'), 123)


if __name__ == '__main__':
    unittest.main()
