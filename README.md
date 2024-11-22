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

* poc for shell

```sh

$ poetry run python  poc_shell.py "How many python files are there in the current directory?"
[nltk_data] Error loading punkt_tab: <urlopen error [Errno 111]
[nltk_data]     Connection refused>
> Running step 71ce7891-50f2-4ca9-a84d-e18dddaa64f0. Step input: How many python files are there in the current directory?
Thought: The current language of the user is: English. I need to use a tool to help me answer the question.
Action: run_shell_command
Action Input: {'command': 'ls | grep .py | wc -l'}
Observation: 2

> Running step 78c7656b-5404-4840-b9d1-463b1d5ce9bb. Step input: None
Thought: I can now infer that there are 2 python files in the current directory. The conversation is complete and no further tools need to be used.
Answer: There are 2 Python files in the current directory.
There are 2 Python files in the current directory.

```

