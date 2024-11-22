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

$ poetry run python  poc_shell.py "How many python files are there in the current directory?" /home/xlisp/Desktop/ai-automatic-env-build
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

* ReAct mechanism

```sh
poc_shell.py "How many png files are there in the current directory?" /home/xlisp/Desktop
[nltk_data] Error loading punkt_tab: <urlopen error [Errno 111]
[nltk_data]     Connection refused>
> Running step 08413b7e-20de-4f70-bd8b-6c208a7f4a98. Step input: How many png files are there in the current directory?
Thought: The current language of the user is English. I need to use a tool to help me answer the question.
Action: run_shell_command
Action Input: {'command': 'ls | grep .png | wc -l'}
Observation: 4

> Running step 191f44e8-1717-42b9-88ef-7fd7280b59e4. Step input: None
Thought: I have some information about the number of png files in the current directory.
Action: run_shell_command
Action Input: {'command': 'ls | grep .txt | wc -l'}
Observation: 0

> Running step d6efd204-b4be-4561-aa6a-fa1ac16b53fd. Step input: None
Thought: I now know there are 4 png files and 0 txt files in the current directory.
I can answer without using any more tools. I'll use the user's language to answer
Answer: There are 4 PNG files in the current directory.
There are 4 PNG files in the current directory.
```

