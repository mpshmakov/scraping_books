import os
import sys
import uuid
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Import statements remain the same
import requests
from database.operations import (
    check_tables_exist,
    engine,
    initDB,
    initialize_schema,
    insert_records,
    insertRow,
)
from database.schema import AcademyAwardWinningFilms, TestTable
from scripts.scraping_books import main, scrape_books
from sqlalchemy.exc import SQLAlchemyError
from wiki import BeautifulSoup, fetchPage
from wiki.export_functions import exportToCsv, exportToJson
from wiki.utils import clean_numeric, create_data_folder, uuid_to_str

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Test Wiki Functions
@patch("requests.get")
def test_fetchPage(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    response = fetchPage("https://google.com")
    assert response.status_code == 200


@patch("requests.get")
def test_fetchPage_exception(mock_get):
    mock_get.side_effect = Exception("Network error")
    with pytest.raises(Exception):
        fetchPage("https://google.com")


# Test Export Functions
@patch("pandas.DataFrame.to_csv")
def test_exportToCsv(mock_to_csv):
    data = {
        "id": ["test-id"],
        "name": ["Test Movie"],
        "year": [2023],
        "awards": [1],
        "nominations": [3],
    }
    df = pd.DataFrame(data)
    exportToCsv(df, "test.csv")
    mock_to_csv.assert_called_once_with("test.csv", index=False)


@patch("json.dump")
def test_exportToJson(mock_json_dump):
    data = {
        "id": ["test-id"],
        "name": ["Test Movie"],
        "year": [2023],
        "awards": [1],
        "nominations": [3],
    }
    df = pd.DataFrame(data)
    exportToJson(df, "test.json")
    mock_json_dump.assert_called_once()


# Test Utils
def test_uuid_to_str():
    test_uuid = uuid.uuid4()
    assert uuid_to_str(test_uuid) == str(test_uuid)
    assert uuid_to_str("not-a-uuid") == "not-a-uuid"


def test_clean_numeric():
    assert clean_numeric("123") == 123
    assert clean_numeric("123.45") == 123
    assert clean_numeric("abc") == "abc"
    assert clean_numeric(456) == 456


# Test Database Operations
@patch("sqlalchemy.inspect")
def test_check_tables_exist(mock_inspect):
    mock_inspect.return_value.get_table_names.return_value = [
        "academy_award_winning_films",
        "TestTable",
    ]
    assert check_tables_exist() == True


@patch("sqlalchemy.orm.Session")
def test_insert_records(mock_session):
    records = [MagicMock(), MagicMock()]
    insert_records(mock_session, records)
    mock_session.add_all.assert_called_once_with(records)
    mock_session.commit.assert_called_once()


@patch("sqlalchemy.orm.Session")
def test_insert_records_exception(mock_session):
    records = [MagicMock(), MagicMock()]
    mock_session.commit.side_effect = SQLAlchemyError()
    with pytest.raises(SQLAlchemyError):
        insert_records(mock_session, records)


@patch("database.operations.initialize_schema")
@patch("database.operations.check_tables_exist")
@patch("database.operations.Session")
def test_initDB(mock_Session, mock_check_tables_exist, mock_initialize_schema):
    mock_check_tables_exist.return_value = True
    mock_session = MagicMock()
    mock_Session.return_value = mock_session

    records = [MagicMock(), MagicMock()]
    initDB(records)

    mock_initialize_schema.assert_called_once()
    mock_check_tables_exist.assert_called_once()
    mock_session.add_all.assert_called_once_with(records)
    mock_session.commit.assert_called_once()


@patch("database.operations.initialize_schema")
@patch("database.operations.check_tables_exist")
@patch("database.operations.Session")
def test_initDB_tables_not_exist(
    mock_Session, mock_check_tables_exist, mock_initialize_schema
):
    mock_check_tables_exist.return_value = False
    records = [MagicMock(), MagicMock()]
    initDB(records)
    mock_initialize_schema.assert_called_once()
    mock_check_tables_exist.assert_called_once()
    mock_Session.assert_not_called()


@patch("database.operations.check_tables_exist")
@patch("database.operations.Session")
def test_insertRow(mock_Session, mock_check_tables_exist):
    mock_check_tables_exist.return_value = True
    mock_session = MagicMock()
    mock_Session.return_value = mock_session

    row = MagicMock()
    row.__tablename__ = "test_table"
    insertRow(row)

    mock_session.add.assert_called_once_with(row)
    mock_session.commit.assert_called_once()


@patch("database.operations.check_tables_exist")
@patch("database.operations.Session")
def test_insertRow_tables_not_exist(mock_Session, mock_check_tables_exist):
    mock_check_tables_exist.return_value = False
    row = MagicMock()
    insertRow(row)
    mock_Session.assert_not_called()


@patch("database.operations.check_tables_exist")
@patch("database.operations.Session")
def test_insertRow_exception(mock_Session, mock_check_tables_exist):
    mock_check_tables_exist.return_value = True
    mock_session = MagicMock()
    mock_Session.return_value = mock_session
    mock_session.commit.side_effect = SQLAlchemyError()

    row = MagicMock()
    row.__tablename__ = "test_table"
    with pytest.raises(SQLAlchemyError):
        insertRow(row)


@patch("database.operations.MetaData")
@patch("database.operations.Table")
@patch("database.operations.engine")
def test_initialize_schema(mock_engine, mock_Table, mock_MetaData):
    mock_metadata = MagicMock()
    mock_MetaData.return_value = mock_metadata

    initialize_schema()

    mock_MetaData.assert_called_once()
    assert mock_Table.call_count == 2  # Called for both tables
    mock_metadata.create_all.assert_called_once_with(mock_engine)


@patch("database.operations.MetaData")
@patch("database.operations.engine")
def test_initialize_schema_exception(mock_engine, mock_MetaData):
    mock_metadata = MagicMock()
    mock_MetaData.return_value = mock_metadata
    mock_metadata.create_all.side_effect = SQLAlchemyError()

    with pytest.raises(SQLAlchemyError):
        initialize_schema()


# Test Database Schema
def test_AcademyAwardWinningFilms():
    film = AcademyAwardWinningFilms("test-id", "Test Film", 2020, 1, 5)
    assert film.id == "test-id"
    assert film.film == "Test Film"
    assert film.year == 2020
    assert film.awards == 1
    assert film.nominations == 5


def test_TestTable():
    test_entry = TestTable("test-id", "Test Entry")
    assert test_entry.id == "test-id"
    assert test_entry.text == "Test Entry"


# Test Wikipedia UUID
@patch("wiki.fetchPage")
@patch("bs4.BeautifulSoup")
def test_scrape_oscar_winning_films(mock_bs, mock_fetchPage):
    mock_response = MagicMock()
    mock_fetchPage.return_value = mock_response
    mock_soup = MagicMock()
    mock_bs.return_value = mock_soup

    mock_tr = MagicMock()
    mock_tr.find_all.return_value = [
        MagicMock(text="Film"),
        MagicMock(text="2020"),
        MagicMock(text="1"),
        MagicMock(text="5"),
    ]
    mock_soup.find.return_value.find.return_value.find_all.return_value = [mock_tr]

    results = scrape_books()
    assert len(results) == 1373
    assert len(results[0]) == 5  # id, film, year, awards, nominations


@patch("scripts.wikipedia_uuid.fetchPage")
def test_scrape_oscar_winning_films_exception(mock_fetchPage):
    mock_fetchPage.return_value = None
    with pytest.raises(Exception) as excinfo:
        scrape_books()

    assert "Failed to fetch the Wikipedia page" in str(excinfo.value)


@patch("scripts.wikipedia_uuid.scrape_oscar_winning_films")
@patch("scripts.wikipedia_uuid.initDB")
@patch("scripts.wikipedia_uuid.insertRow")
@patch("scripts.wikipedia_uuid.exportToCsv")
@patch("scripts.wikipedia_uuid.exportToJson")
def test_main(
    mock_exportToJson, mock_exportToCsv, mock_insertRow, mock_initDB, mock_scrape
):
    mock_scrape.return_value = [
        ("id1", "Film 1", 2021, 1, 3),
        ("id2", "Film 2", 2022, 2, 5),
    ]
    main()
    mock_scrape.assert_called_once()
    mock_initDB.assert_called_once()
    assert mock_insertRow.call_count == 2
    mock_exportToCsv.assert_called_once()
    mock_exportToJson.assert_called_once()
