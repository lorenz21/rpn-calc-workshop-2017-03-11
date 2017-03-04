# pylint: disable=C0103,C0111,W0212

import unittest
import rpncalculator


class TestOperandStack(unittest.TestCase):

    def setUp(self):
        self.engine = rpncalculator.Engine()

    def test_stack_exists(self):
        self.assertIsNotNone(self.engine._stack)
        self.assertIsInstance(self.engine._stack, list)
        self.assertEqual(len(self.engine._stack), 0)


class TestPush(unittest.TestCase):

    def setUp(self):
        self.engine = rpncalculator.Engine()

    def test_push_exists(self):
        self.assertTrue(callable(self.engine.push))
        self.assertIsNotNone(self.engine.push(0))

    def test_push_changes_stack_size(self):
        self.engine.push(0)
        self.assertEqual(len(self.engine._stack), 1)

    def test_push_returns_pushed_value(self):
        self.assertEqual(self.engine.push(123), 123)

    def test_push_adds_item_to_end_of_stack(self):
        stack = self.engine._stack
        for i in range(5):
            self.engine.push(i)
            self.assertEqual(stack[-1], i)
            self.assertEqual(len(stack), i+1)

    def test_push_only_allows_numerical_values(self):
        self.engine.push(0)
        self.engine.push(0.)
        with self.assertRaises(rpncalculator.InvalidValueTypeError):
            self.engine.push('')
        with self.assertRaises(rpncalculator.InvalidValueTypeError):
            self.engine.push(list())
        with self.assertRaises(rpncalculator.InvalidValueTypeError):
            self.engine.push(set())
        with self.assertRaises(rpncalculator.InvalidValueTypeError):
            self.engine.push(object())
        with self.assertRaises(rpncalculator.InvalidValueTypeError):
            self.engine.push(self.setUp)


class TestPop(unittest.TestCase):

    def setUp(self):
        self.engine = rpncalculator.Engine()

    def test_pop_exists(self):
        self.assertTrue(callable(self.engine.pop))

    def test_pop_empty_stack_returns_none(self):
        self.assertIsNone(self.engine.pop())

    def test_pop_returns_top_of_stack(self):
        self.engine._stack = list(range(5))
        stack = self.engine._stack
        for i in range(5, 0, -1):
            result = self.engine.pop()
            self.assertEqual(result, i-1)
            self.assertEqual(len(stack), i-1)


def null_operation(engine):  # pylint: disable=W0613
    return


def no_parameter_function():
    return


def two_parameter_function(engine, x):  # pylint: disable=W0613
    return


def wrong_parameter_name_function(x):  # pylint: disable=W0613
    return


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.engine = rpncalculator.Engine(auto_register=False)

    def test_register_exists(self):
        self.assertTrue(callable(self.engine.register))

    def test_operations_table_exists(self):
        self.assertIsNotNone(self.engine._operations)
        self.assertIsInstance(self.engine._operations, dict)

    def test_operation_table_includes_noop_function_only(self):
        self.assertEqual(len(self.engine._operations), 1)
        self.assertTrue('noop' in self.engine._operations)

    def test_register_inserts_definition_into_table(self):
        operation = 'x'
        function = null_operation
        self.engine.register(operation, function)
        self.assertEqual(len(self.engine._operations), 2)
        self.assertEqual(self.engine._operations[operation], function)

    def test_register_does_not_replace_existing_function(self):
        operation = 'x'
        function = null_operation
        self.engine.register(operation, function)
        with self.assertRaises(rpncalculator.DuplicateOperationError):
            self.engine.register(operation, function)

    def test_register_rejects_function_with_wrong_number_of_parameters(self):
        with self.assertRaises(rpncalculator.InvalidOperationSignatureError):
            self.engine.register('x', no_parameter_function)
        with self.assertRaises(rpncalculator.InvalidOperationSignatureError):
            self.engine.register('x', two_parameter_function)

    def test_register_rejects_function_with_wrong_parameter_name(self):
        with self.assertRaises(rpncalculator.InvalidOperationSignatureError):
            self.engine.register('x', wrong_parameter_name_function)


def add(engine):
    engine.push(engine.pop() + engine.pop())


class TestExecute(unittest.TestCase):

    def setUp(self):
        self.engine = rpncalculator.Engine()

    def test_execute_exists(self):
        self.assertTrue(callable(self.engine.execute))

    def test_add(self):
        self.engine.register('add', add)
        self.engine.push(1)
        self.engine.push(1)
        result = self.engine.execute('add')
        self.assertEqual(result, 2)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), 2)


if __name__ == '__main__':
    unittest.main()
