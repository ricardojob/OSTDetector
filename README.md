[![Tests](https://github.com/ricardojob/psae/actions/workflows/tests.yaml/badge.svg)](https://github.com/ricardojob/ostdetector/actions/workflows/tests.yaml)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psae)](https://pypi.org/project/ostdetector/)

# OSTDetector

An automated tool for extracting OS-specific Tests from Git repositories written in Python. 
The `ostdetector` (**O**perating System-**S**pecific **T**ests **D**etector) is primarily designed to be used as a command-line tool. 
With `ostdetector`, you can easily extract information about the OS-specific Tests from the Git repository (only python files are analyzed).
The set of OS-specific Tests are saved in a given CSV file.

## Install

The easiest way to install `ostdetector` is to install from Pypi

```
pip install -i https://test.pypi.org/simple/ ostdetector==1.0.5
```

Alternatively, you can install from `test environment`
```
pip install --index-url https://test.pypi.org/simple/ --no-deps ostdetector
```

You may wish to use this tool in a virtual environment. You can use the following commands.

```
virtualenv ostdetector_venv
source ostdetector_venv/bin/activate
pip install ostdetector
```

## Quick examples

As an example, the following command extracts every OS-Specific Testes from the repository `ricardojob/ostdetector`. 
It also saves various information (line, module, filename ...) in directory `dir_output`. 
This information will be available in the output file.

```bash
ostdetector ricardojob/ostdetector -o dir_output
```

Note that the tool also can fetch it. 
For example, the GitHub repository `https://github.com/ricardojob/ostdetector` will be fetched, saved under the `dir_output/ricardojob` directory.
Note that, by default all projects are cloned to the `data` directory.


## Usage

After installation, the `ostdetector` command-line tool should be available in your shell. 
Otherwise, please replace `ostdetector` by `python -m ostdetector`. 
The explanations in the following stays valid in both cases.

You can use `ostdetector` with the following arguments:

```
Usage: ostdetector [OPTIONS] REPOSITORY

  Extract the usage of OS-Specific Tests from a single Git repository
  `REPOSITORY`. The Git repository can be remote. It will be pulled locally in
  the folder `data`. Every extracted OS-Specific Tests will be written in the
  dir given to `-o`, or in the `data' if not specified.

  Example of usage: python main.py ricardojob/OSTDetector -o data_experiment

Options:
  -o, --output DIRECTORY  The output dir where the usage of OS-Specific Tests
                          related to the repository will be stored. By
                          default, the information will written to `data' dir.
  -h, --help              Show this message and exit.
```

The `*compare.csv' file given to directory `-o` will contain the following columns:
- `project_name`: the name of the repository
- `project_hash`: the commit SHA of the commit where the OS-specific tests file was extracted
- `line`: the line where the OS-specific tests usage occurs
- `module`: the module that packages the OS-specific tests (e.g., sys)
- `package`: the API (e.g., platform)
- `platform`: the information about OS (e.g, win32)
- `file`: the file name
- `function`: the function name
- `method_type`: the method type (method_test or support)
- `url`: the URL that represents the API usage on Github

## License

Distributed under [MIT License](https://github.com/ricardojob/ostdetector/blob/main/LICENSE.txt).