import unittest

import rpncalculator
from rpncalculator.functions import register_all


class TestFunctionRegisterAll(unittest.TestCase):

    def setUp(self):
        self.engine = rpncalculator.Engine(auto_register=False)

    def test_register_function_finds_add(self):
        register_all(self.engine)
        with self.assertRaises(rpncalculator.errors.DuplicateOperationError):
            self.engine.register('+', lambda engine: None)


if __name__ == '__main__':
    unittest.main()
