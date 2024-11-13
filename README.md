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

