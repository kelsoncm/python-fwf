How to contribute
=================

.. code-block:: bash
    git clone git@github.com:kelsoncm/sc4.git ~/projetos/PESSOAL/sc4py
    code ~/projetos/PESSOAL/sc4py

Pre-commit
----------

This repository uses [pre-commit](https://pre-commit.com/) to run quality checks
before each commit and coverage regression checks before each push.

**Setup:**

.. code-block:: bash
    python -m venv .venv
    .venv\bin\activate
    .\.venv\Scripts\Activate.ps1
    pip install --upgrade pip uv
    uv pip install --upgrade -e ".[dev]"
    pre-commit install
    pre-commit install --hook-type pre-push

Run manually:

.. code-block:: bash
    pre-commit run --all-files
    pre-commit run --hook-stage pre-push --all-files

**Hooks:**

* **pre-commit**
   * `trailing-whitespace` for eliminating trailing whitespace
   * `end-of-file-fixer` for ensuring files end with a newline
   * `check-yaml` for validating YAML files
   * `check-added-large-files` for preventing large files from being committed
   * `black` for code formatting
   * `ruff` for linting and static analysis
   * `doc8` for checking documentation style
   * `markdownlint` for checking Markdown style
* **pre-push**:
   * `pytest` for running tests
   * `pytest-coverage-gate` for checking test coverage
* **GitHub Actions only**
   * `semgrep` for security and code quality checks
