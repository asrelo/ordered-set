# Developer documentation

## Automation with **tox**

**tox** is used to automate some tasks, like testing on different versions of Python.

Be aware, the config allows **tox** to skip some environments when the required version of Python is not available. You can make it always require the interpreters with a command line option `-s false` ([skip_missing_interpreters](https://tox.wiki/en/stable/config.html#skip_missing_interpreters)).

## Unit tests

**pytest** powers the unit tests. All extra dependencies for testing are grouped as `test` extra dependencies.

Unit tests require the custom plugin for **pytest** &mdash; `asrelo-pytest-universal-indirection`. You can fetch it from GitHub: [asrelo/pytest-universal-indirection](https://github.com/asrelo/pytest-universal-indirection).

### Manually from an environment (fast)

To run unit tests from an environment:

    pytest

### Via **tox**

To run unit tests on a specific version of Python (e.g. 3.12) via **tox** (slow):

    tox run -e 3.12

To run unit tests on different supported version of Python via **tox** (very slow):

    tox

### Coverage report

**coverage.py** is used to track code coverage by tests. All extra dependencies for coverage reporting are grouped among `test` extra dependencies.

To acquire a coverage report with **coverage.py**, you generally need to:

1. run the tests under control of **coverage.py**, collecting coverage data;
2. combine data from different runs;
3. build a report.

#### Via **tox**

Coverage data is collected unconditionally when unit tests are run via **tox** (see above).

To work on coverage data, you need some dependencies to be installed independently. Install requirements from the file `requirements/requirements-coverage-report.txt` (into an environment).

To combine coverage data from different runs:

    coverage combine

To produce an HTML coverage report (placed into `coverage_report/html`):

    coverage html

To produce a text coverage report (printed into the terminal):

    coverage report

#### Manually from an environment

To collect coverage data when running unit tests from an environment:

    coverage run [-p] -m <pytest command>

Replace `<pytest command>` with the **pytest** command you want to use (see above).

The flag `-p` is used when one runs tests multiple times and wants combine data from different runs. See [CLI docs](https://coverage.readthedocs.io/en/7.10.0/cmd.html#execution-coverage-run).

For instructions on how to use coverage data to produce reports, see the section above "Via **tox**", assuming you already have `coverage` available in your environment.

## Linting

**flake8** is used to lint the code. All extra dependencies for linting are grouped among `dev` extra dependencies.

To lint the code via **tox**:

    tox lint

To lint the code from an environment:

    flake8 --extend-ignore=PT ordered_set/; \
        flake8 conftest.py tests/

Use of the autoformatter **Black** was considered, but it's got some weird unconfigurable and even undocumented rules (like leaving an extra blank line *after* every comment *inside* a function). I don't like these rules and don't trust **Black** because the docs imply that all significant rules are documented.

## Building distribution packages

To build distribution packages (sdist and wheel):

    python -m build

## To do

This project already took me like 20 times more time than was needed to cover any of my own possible requirements.

Below are major deeds that can be worth to do, in no particular order.

* Add "ordered dict" types.

* Write user documentation:

  * docstrings;

  * usage tutorial.

* Build pretty docs with [**Sphinx**](https://www.sphinx-doc.org/).

* Complete typing of the code.

  * Start using the type checker [**mypy**](https://mypy-lang.org/).

* Create benchmarks (complexity evaluation?).

* Start using the **Git** hooks manager [**pre-commit**](https://pre-commit.com/) (see the file `.pre-commit-config.yaml.unused`).

* Start using CI/CD via **GitHub Actions**.
