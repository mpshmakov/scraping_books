## Wikipedia Film Data Acquirer

This project, the `Wikipedia Film Data Acquirer`, is a sophisticated tool designed to systematically harvest and collate information about films from Wikipedia, providing cinephiles and researchers with a rich dataset for analysis and exploration of cinematic history and trends.

### Install Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following

```python
## Prerequisites
python3 -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
python3 -m pip install --upgrade pip
deactivate
```

### Usage

```python
## Actual Application
python3 -m scripts.wikipedia_uuid

## Unit Test with Coverage
coverage run -m unittest discover

## Generate Coverage Report
coverage report -m

## Pytest
pytest
```

> You can keep the `data` directory. It's a small project, so you are not storing large files in the repository.

### Current Code Coverage

| Name | Stmts | Miss | Cover | Missing |
|------|-------|------|-------|---------|
| database/__init__.py | 17 | 0 | 100% | |
| database/operations.py | 77 | 7 | 91% | 128-131, 134-136 |
| database/schema.py | 24 | 0 | 100% | |
| scripts/wikipedia_uuid.py | 67 | 12 | 82% | 35, 51, 54, 71-72, 84-85, 101-104, 107 |
| tests/__init__.py | 205 | 12 | 94% | 21-24, 27-28, 31-32, 35-36, 39, 247 |
| wiki/__init__.py | 19 | 2 | 89% | 44-45 |
| wiki/export_functions.py | 15 | 0 | 100% | |
| wiki/utils.py | 19 | 2 | 89% | 21-22 |
| **TOTAL** | **440** | **35** | **92%** | |

### Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/moatsystems/imdb_scrapy/tags).


### License

This project is licensed under the [BSD 3-Clause License](LICENSE) - see the file for details.

### Copyright

(c) 2024 [Maksim Shmakov](https://coming.com).
