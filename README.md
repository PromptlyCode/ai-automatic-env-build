# AI Automatic Environment Build

* Why: AI automatic environment construction and repair, ReAct mechanism,  automatically execute AI programs such as shell, python, and interact with the environment to return answer results multiple times

## Features

- [x] Automatically generate shell, correct environmental problems and environmental questions: for example, ask how many python files are there in a directory
- [x] AI generates python, corrects environmental problems and learns code, POC fast verification: for example, write a Python algorithm based on the data in the project code.
- [x] Integration provides API for VSCode and Emacs extension, use command

## Init

* Setup python env
```sh
conda create -n  ai-automatic-env-build python=3.11
conda activate  ai-automatic-env-build
poetry install
```

## Usage

* ReAct mechanism, poc for shell

```sh
$ poetry run python  poc_shell.py "How many image files are there in the current directory?" /home/xlisp/Desktop
[nltk_data] Error loading punkt_tab: <urlopen error [Errno 111]
[nltk_data]     Connection refused>
> Running step 401c0607-be8e-44ea-9c2d-1f4443be5775. Step input: How many image files are there in the current directory?
Thought: The current language of the user is: English. I need to use a tool to help me answer the question.
Action: run_shell_command
Action Input: {'command': 'ls -1 *.jpg | wc -l; ls -1 *.png | wc -l; ls -1 *.gif | wc -l; ls -1 *.jpeg | wc -l'}
Observation: 0
4
0
0

> Running step 4f5afda5-a519-4d59-91de-6021f114af41. Step input: None
Thought: I can parse the output of the shell command to get the total count of image files.
Action: add
Action Input: {'a': 0, 'b': 4}
Observation: 4
> Running step cf0adec5-7b39-42b0-bf00-35f626787d07. Step input: None
Thought: The total count of image files in the current directory is already calculated by adding up all counts. No further action needed.
Answer: There are 4 image files in the current directory.
There are 4 image files in the current directory.

```

* poc for python, look: calculator_pro/

```
$ poetry run python poc_python_autogen.py -r "Create a Calculator class with basic arithmetic operations" -w calculator_pro

Generating project...
Writing code to: calculator_pro/calculator.py

Code Review:
I'll review the code and provide feedback on different aspects:

**Positive Aspects:**
1. Well-structured and organized code with clear class and method definitions
2. Comprehensive docstrings following good documentation practices
3. Type hints are used consistently throughout the code
4. Good error handling for division by zero
5. Clear separation of concerns with distinct methods for different operations
6. Includes example usage and test cases
7. Good use of memory functionality for calculator operations
8. Clean implementation of basic arithmetic operations

**Suggestions for Improvement:**

1. **Input Validation:**
'''python
def add(self, x: float, y: float) -> float:
    # Add input validation
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Arguments must be numbers")
    self.last_result = x + y
    return self.last_result
'''

2. **Constants Definition:**
'''python
class Calculator:
    DEFAULT_VALUE = 0  # Define constants at class level

    def __init__(self):
        self.memory = self.DEFAULT_VALUE
        self.last_result = self.DEFAULT_VALUE
'''

3. **Property Decorators:**
'''python
@property
def last_result(self) -> float:
    return self._last_result

@last_result.setter
def last_result(self, value: float) -> None:
    self._last_result = value
'''

4. **Add Testing Framework:**
'''python
import unittest
class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
'''

5. **Method Return Type Consistency:**
- Consider returning `self` from methods like `clear()`, `store_in_memory()`, and `clear_memory()` to enable method chaining

6. **Add Rounding Control:**
'''python
def __init__(self, precision: int = 10):
    self.memory = 0
    self.last_result = 0
    self.precision = precision

def _round_result(self, value: float) -> float:
    return round(value, self.precision)
'''

7. **Add More Advanced Features:**
- Consider adding support for operations with multiple numbers
- Add support for mathematical functions (square root, power, etc.)

8. **Error Messages:**
'''python
class CalculatorError(Exception):
    """Custom exception for calculator errors"""
    pass

# Use custom exception
if y == 0:
    raise CalculatorError("Division by zero is not allowed")
'''

9. **Add Context Manager Support:**
'''python
def __enter__(self):
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    self.clear()
'''

10. **Add Logging:**
'''python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add(self, x: float, y: float) -> float:
    logger.debug(f"Adding {x} and {y}")
    self.last_result = x + y
    return self.last_result
'''

**Security Considerations:**
- Consider adding input sanitization if the calculator will be used with user input
- Add bounds checking for very large numbers to prevent overflow
- Consider adding protection against floating-point precision errors

**Performance Considerations:**
- The current implementation is efficient for basic calculations
- For heavy usage, consider caching frequently used results
- For complex calculations, consider using decimal.Decimal for better precision

The code is well-written overall, but implementing some of these suggestions would make it more robust and feature-complete. The choice of which improvements to implement would depend on the specific use case and requirements of the project.
Writing code to: calculator_pro/test_calculator.py

Running tests from test_calculator.py...
========================================================================= test session starts =========================================================================
platform darwin -- Python 3.11.10, pytest-8.3.3, pluggy-1.5.0 -- /opt/anaconda3/envs/ai-automatic-env-build/bin/python
cachedir: .pytest_cache
rootdir: /Users/clojure/Desktop/ai-automatic-env-build
configfile: pyproject.toml
plugins: anyio-4.6.2.post1
collected 12 items

calculator_pro/test_calculator.py::TestCalculator::test_initialization PASSED                                                                                   [  8%]
calculator_pro/test_calculator.py::TestCalculator::test_add PASSED                                                                                              [ 16%]
calculator_pro/test_calculator.py::TestCalculator::test_subtract PASSED                                                                                         [ 25%]
calculator_pro/test_calculator.py::TestCalculator::test_multiply PASSED                                                                                         [ 33%]
calculator_pro/test_calculator.py::TestCalculator::test_divide PASSED                                                                                           [ 41%]
calculator_pro/test_calculator.py::TestCalculator::test_divide_by_zero PASSED                                                                                   [ 50%]
calculator_pro/test_calculator.py::TestCalculator::test_clear PASSED                                                                                            [ 58%]
calculator_pro/test_calculator.py::TestCalculator::test_get_last_result PASSED                                                                                  [ 66%]
calculator_pro/test_calculator.py::TestCalculator::test_memory_operations PASSED                                                                                [ 75%]
calculator_pro/test_calculator.py::TestCalculator::test_floating_point_precision PASSED                                                                         [ 83%]
calculator_pro/test_calculator.py::TestCalculator::test_negative_numbers PASSED                                                                                 [ 91%]
calculator_pro/test_calculator.py::TestCalculator::test_operation_sequence PASSED                                                                               [100%]

========================================================================== warnings summary ===========================================================================
../../../../opt/anaconda3/envs/ai-automatic-env-build/lib/python3.11/site-packages/_pytest/config/__init__.py:1277
  /opt/anaconda3/envs/ai-automatic-env-build/lib/python3.11/site-packages/_pytest/config/__init__.py:1277: PytestAssertRewriteWarning: Module already imported so cannot be rewritten: anyio
    self._mark_plugins_for_rewrite(hook)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
==================================================================== 12 passed, 1 warning in 0.05s ====================================================================

Project generation completed!
Main implementation: calculator.py
Test file: test_calculator.py

```

* poc for web

```sh
$  poetry run python poc_web_autogen.py  -r "Create a Calculator class with basic arithmetic operations" -w calculator_web_pro
Setting up project structure...
Generating web components...
Writing files...
Setting up testing environment...
(node:40068) ExperimentalWarning: CommonJS module /usr/local/lib/node_modules/npm/node_modules/debug/src/node.js is loading ES Module /usr/local/lib/node_modules/npm/node_modules/supports-color/index.js using require().
Support for loading ES Module in require() is an experimental feature and might change at any time
(Use `node --trace-warnings ...` to show where the warning was created)
npm warn deprecated abab@2.0.6: Use your platform's native atob() and btoa() methods instead
npm warn deprecated domexception@4.0.0: Use your platform's native DOMException instead

added 407 packages, and audited 408 packages in 4m

35 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
Running tests...

> web-project@1.0.0 test
> jest

 FAIL  tests/app.test.js
  ● Test suite failed to run

    Cannot find module '@testing-library/jest-dom' from 'tests/app.test.js'

    > 1 | require('@testing-library/jest-dom');
        |                                     ^

      at Resolver._throwModNotFoundError (node_modules/jest-resolve/build/resolver.js:427:11)
      at Object.<anonymous> (tests/app.test.js:1:37)

Test Suites: 1 failed, 1 total
Tests:       0 total
Snapshots:   0 total
Time:        1.082 s
Ran all test suites.
(node:40509) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
Error running tests: Command '['npm', 'test']' returned non-zero exit status 1.

Project generation completed!
Project location: calculator_web_pro

```
