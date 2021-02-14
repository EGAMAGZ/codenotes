# Codenotes
*All your annotations without quitting the terminal*

[![PyPI version](https://badge.fury.io/py/Codenotes.svg)](https://badge.fury.io/py/Codenotes)
![PyPI - License](https://img.shields.io/pypi/l/codenotes)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/codenotes)
![PyPI - Status](https://img.shields.io/pypi/status/codenotes)

A simple CLI where you can save and view all your created annotations

## Installation
To install `codenotes`, it is recommended to use pip:
```
pip install codenotes
```
You can install it from source. Clone this repository and use pip to install:
```
git clone https://github.com/EGAMAGZ/codenotes.git
cd codenotes
pip install .
```

If `codenotes` is already installed and you would like to update it, use:
```
pip install --upgrade codenotes
```
If updating local version, use:
```
cd codenotes
git pull
pip install --upgrade .
```
## Usage
Run `codenotes` to display the usage text.

```
codenotes <action> <annotation> <flags>
```
<img src="images/CodenotesSample.gif">

**Features**
* Creates notes and tasks, and saves them in a category optionally specified
* Shows a preview of the annotation creation
* Creates categories where tasks or notes will be saved
* Searches for annotations created today, yesterday, during the week or month

## Unit Tests
`codenotes` unit tests are written for `unittest`. To run the tests:
```
python -m unittest
```

## License
MIT License

Copyright (c) 2021 Gamaliel Garcia
