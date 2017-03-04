# RPN Calculator Engine for Python Workshops

The purpose of this project is to create a generalized calculator engine for
use in Python workshops teaching how to use `git`, pull requests, and other
open-source contribution processes.


## The Calculator

This calculator uses
[Reverse-Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
to express functions.


## Sample Usage

Instantiate the calculator, then apply operations by calling `push()` and
`execute()`. The only built-in functions are `noop` (no-operation), `+` (add),
and `/` (floating-point division); additional desired functionality can be
registered as needed (see **Extending the Calculator**).

    import rpncalculator
    
    calc = rpncalculator.Engine()
    calc.push(1)
    calc.execute('noop')
    calc.push(2)
    calc.push(3)
    calc.execute('+')  # returns 5

To get a bare-bones calculator with no registered functions other than `noop`,
pass `auto_register=False` to the constructor:

    import rpncalculator
    
    calc = rpncalculator.Engine(auto_register=False)
    calc.execute('noop')  # succeeds
    calc.execute('+')     # fails, function is not defined


## Unit Tests

### Installing the test harness

You might need to install `setuptools` in your environment:

    pip install setuptools

Once `setuptools` is installed, all testing is handled through `setup.py`.

### Running the test suite

The easiest way to run the test suite is using `setup.py`:

    python setup.py test

### Adding new tests

If new tests need to be added to the project, put them in `test/<module_name>.py`
and add `from <module_name> import *` to `test/__init__.py`.


## Extending the Calculator

Additional functions can be added to the calculator using the
`register(name, function)` function:

    def add(engine):
        engine.push(engine.pop() + engine.pop())
    
    calc.register('+', add)

Registered functions must have the signature `fn(engine)` or the call to
`register` will fail. An attempt to register the same function name twice will
throw an error. The function may perform any sequence of calls to `push`,
`pop`, and `execute`; however, to be RPN-correct it should only `pop` exactly
the number of times needed to retrieve the necessary values and then `push`
once (performing necessary algorithmic steps in-between).


## Using the Parser

Instead of interacting programmatically with the calculator, you can also
supply input as a string or as an open file object:

    import rpncalculator
    
    # Note: this example assumes the '+' operation has been registered
    # as previously demonstrated.
    
    parser = rpncalculator.Parser()
    result = parser.process('1 1 +')    # result = 2
    
    with open(myinputfile) as f:
        result = parser.process(f)

Files can be arbitrarily large; the tokenization engine is smart about only
tokenizing small chunks of the input at a time.
