## Scraping Books

Books to Scrape is a mock online bookstore designed for web scraping activities. It offers a diverse catalog of books across various genres, complete with pricing, availability, and star ratings, making it an excellent resource for engineers to sharpen their data extraction skills.

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
python3 -m scripts.scraping_books

## Unit Test with Coverage
coverage run -m pytest

## Generate Coverage Report
coverage report -m

## Pytest
pytest
```

> You can keep the `data` directory. It's a small project, so you are not storing large files in the repository.

### Current Code Coverage

| Name                              | Stmts   | Miss   | Cover   | Missing                                      |
| --------------------------------- | ------- | ------ | ------- | -------------------------------------------- |
| configuration.py                  | 7       | 0      | 100%    |                                              |
| database\_\_init\*\*.py           | 16      | 0      | 100%    |                                              |
| database\operations.py            | 76      | 7      | 91%     | 132-135, 138-142                             |
| database\schema.py                | 26      | 0      | 100%    |
| sbooks\_\_init\*\*.py             | 17      | 2      | 88%     | 42-43                                        |
| sbooks\export_functions.py        | 17      | 0      | 100%    |                                              |
| sbooks\utils.py                   | 23      | 2      | 91%     | 32-33                                        |
| scripts\scraping_books.py         | 136     | 10     | 93%     | 168, 201-202, 214-215, 233-236, 240          |
| tests\_\_init\_\_.py              | 0       | 0      | 100%    |                                              |
| tests\scraping_books_data_test.py | 199     | 14     | 93%     | 33-36, 39-40, 43-44, 47-48, 51, 288-289, 330 |
| **TOTAL**                         | **517** | **35** | **93%** |                                              |

### Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/moatsystems/imdb_scrapy/tags).

### License

This project is licensed under the [BSD 3-Clause License](LICENSE) - see the file for details.

### Copyright

(c) 2024 [Maksim Shmakov](https://coming.com).
