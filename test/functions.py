import unittest
import rpncalculator


class TestFunction(unittest.TestCase):

    def setUp(self):
        self.engine = rpncalculator.Engine()


class TestAdd(TestFunction):

    def test_add(self):
        self.engine.push(1)
        self.engine.push(1)
        result = self.engine.execute('+')
        self.assertEqual(result, 2)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), 2)


class TestDivide(TestFunction):

    def setUp(self):
        super(TestDivide, self).setUp()

    def test_divide(self):
        self.engine.push(12)
        self.engine.push(3)
        result = self.engine.execute('/')
        self.assertEqual(result, 4)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), 4)

    def test_rational_division(self):
        self.engine.push(15)
        self.engine.push(6)
        result = self.engine.execute('/')
        self.assertEqual(result, 2.5)

    def test_divide_by_zero(self):
        self.engine.push(1)
        self.engine.push(0)
        with self.assertRaises(ZeroDivisionError):
            self.engine.execute('/')


class TestMultiplication(TestFunction):

    def test_multiplication(self):
        self.engine.push(2)
        self.engine.push(3)
        result = self.engine.execute('*')
        self.assertEqual(result, 6)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), 6)

    def test_multiplication_zero(self):
        self.engine.push(2)
        self.engine.push(0)
        result = self.engine.execute('*')
        self.assertEqual(result, 0)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), 0)


class TestNegate(TestFunction):

    def setUp(self):
        super(TestNegate, self).setUp()

    def test_negate(self):
        self.engine.push(4)
        result = self.engine.execute('neg')
        self.assertEqual(result, -4)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), -4)

    def test_negate_zero(self):
        self.engine.push(0)
        result = self.engine.execute('neg')
        self.assertEqual(result, 0)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), 0)

    def test_negate_negative(self):
        self.engine.push(-4)
        result = self.engine.execute('neg')
        self.assertEqual(result, 4)
        self.assertEqual(len(self.engine._stack), 1)
        self.assertEqual(self.engine.pop(), 4)


if __name__ == '__main__':
    unittest.main()
