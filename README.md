# AI Automatic Environment Build

* Why: AI automatic environment construction and repair, ReAct mechanism,  automatically execute AI programs such as shell, python, and interact with the environment to return answer results multiple times

## Features

- [x] Automatically generate shell, correct environmental problems and environmental questions: for example, ask how many python files are there in a directory
- [x] AI generates python, corrects environmental problems and learns code, POC fast verification: for example, write a Python algorithm based on the data in the project code.
- [ ] Integration provides API for VSCode and Emacs extension

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

* poc for python, look: calculator_project/

```sh
 poc_python_autogen.py -r "Create a Calculator class with basic arithmetic operations" -w
 calculator_project
Generating project...

Code Review:
I'll review the code for different aspects:

**Positive Aspects:**
1. Good code organization and class structure
2. Comprehensive docstrings following Google's style guide
3. Proper type hints for method parameters and return values
4. Good error handling for division by zero
5. Clear and descriptive method names
6. Good separation of concerns with a main() function
7. Proper use of if __name__ == "__main__" idiom
8. Clean and consistent formatting

**Suggestions for Improvement:**

1. **Empty __init__ Method:**
```python
def __init__(self):
    pass
```
Since the __init__ method is empty, it can be removed entirely as Python will provide a default constructor.

2. **Input Validation:**
Consider adding input validation for non-numeric inputs:
```python
def add(self, x: float, y: float) -> float:
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Arguments must be numbers")
    return x + y
```

3. **Power Method Safety:**
The power method could use additional error handling:
```python
def power(self, x: float, y: float) -> float:
    try:
        return x ** y
    except OverflowError:
        raise ValueError("Result too large to compute")
```

4. **Constants:**
Consider adding class-level constants for frequently used values:
```python
class Calculator:
    DECIMAL_PRECISION = 10  # if needed for rounding
```

5. **Testing:**
Consider adding unit tests in a separate file to test edge cases and normal operations.

6. **Main Function Structure:**
The main function could be structured better to separate test cases:
```python
def main():
    calc = Calculator()

    def run_tests():
        test_cases = [
            ("Addition", lambda: calc.add(5, 3)),
            ("Subtraction", lambda: calc.subtract(10, 4)),
            # ... more test cases
        ]

        for name, operation in test_cases:
            try:
                result = operation()
                print(f"{name}: {result}")
            except Exception as e:
                print(f"{name} Error: {e}")

    run_tests()
```

7. **Optional Enhancements:**
- Add a method to round results to a specified precision
- Add memory functionality (like a basic calculator's M+, M-, MR buttons)
- Add support for operation chaining
- Add a method to get operation history

8. **Documentation:**
Consider adding examples in docstrings:
```python
def add(self, x: float, y: float) -> float:
    """
    Add two numbers.

    Args:
        x (float): First number
        y (float): Second number

    Returns:
        float: Sum of x and y

    Example:
        >>> calc = Calculator()
        >>> calc.add(5, 3)
        8.0
    """
    return x + y
```

Overall, this is a well-written piece of code that follows many Python best practices. The suggestions above would make it more robust and production-ready, but the current implementation is already solid for basic calculator functionality.

Running tests...
========================================================================= test session starts =========================================================================
platform darwin -- Python 3.11.10, pytest-8.3.3, pluggy-1.5.0 -- /opt/anaconda3/envs/ai-automatic-env-build/bin/python
cachedir: .pytest_cache
rootdir: /Users/clojure/Desktop/ai-automatic-env-build
configfile: pyproject.toml
plugins: anyio-4.6.2.post1
collected 0 items / 1 error

...
test_main.py:103: AssertionError
======================================================================= short test summary info =======================================================================
FAILED test_main.py::TestCalculator::test_operations_return_float - assert False
==================================================================== 1 failed, 25 passed in 0.13s =====================================================================

```
