import os
import sys
import unittest
import uuid
from unittest.mock import MagicMock, patch

import pandas as pd
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


class WikiFilmDataTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "test_results")
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_file = open(os.path.join(self.output_dir, "test_results.txt"), "w")

    def addSuccess(self, test):
        super().addSuccess(test)
        self.output_file.write(f"PASS: {test}\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.output_file.write(f"ERROR: {test}\n{err}\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.output_file.write(f"FAIL: {test}\n{err}\n")

    def close(self):
        self.output_file.close()


class TestWikiFunctions(unittest.TestCase):
    @patch("requests.get")
    def test_fetchPage(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        response = fetchPage("https://google.com")
        self.assertEqual(response.status_code, 200)

    @patch("requests.get")
    def test_fetchPage_exception(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        with self.assertRaises(Exception):
            fetchPage("https://google.com")


class TestExportFunctions(unittest.TestCase):
    @patch("pandas.DataFrame.to_csv")
    def test_exportToCsv(self, mock_to_csv):
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
    def test_exportToJson(self, mock_json_dump):
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


class TestUtils(unittest.TestCase):
    def test_uuid_to_str(self):
        test_uuid = uuid.uuid4()
        self.assertEqual(uuid_to_str(test_uuid), str(test_uuid))
        self.assertEqual(uuid_to_str("not-a-uuid"), "not-a-uuid")

    def test_clean_numeric(self):
        self.assertEqual(clean_numeric("123"), 123)
        self.assertEqual(clean_numeric("123.45"), 123)
        self.assertEqual(clean_numeric("abc"), "abc")
        self.assertEqual(clean_numeric(456), 456)


class TestDatabaseOperations(unittest.TestCase):
    @patch("sqlalchemy.inspect")
    def test_check_tables_exist(self, mock_inspect):
        mock_inspect.return_value.get_table_names.return_value = [
            "academy_award_winning_films",
            "TestTable",
        ]
        self.assertTrue(check_tables_exist())

    # @patch('sqlalchemy.inspect')
    # def test_check_tables_not_exist(self, mock_inspect):
    #     mock_inspect.return_value.get_table_names.return_value = []
    #     self.assertFalse(check_tables_exist())

    @patch("sqlalchemy.orm.Session")
    def test_insert_records(self, mock_session):
        records = [MagicMock(), MagicMock()]
        insert_records(mock_session, records)
        mock_session.add_all.assert_called_once_with(records)
        mock_session.commit.assert_called_once()

    @patch("sqlalchemy.orm.Session")
    def test_insert_records_exception(self, mock_session):
        records = [MagicMock(), MagicMock()]
        mock_session.commit.side_effect = SQLAlchemyError()
        with self.assertRaises(SQLAlchemyError):
            insert_records(mock_session, records)

    @patch("database.operations.initialize_schema")
    @patch("database.operations.check_tables_exist")
    @patch("database.operations.Session")
    def test_initDB(
        self, mock_Session, mock_check_tables_exist, mock_initialize_schema
    ):
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
        self, mock_Session, mock_check_tables_exist, mock_initialize_schema
    ):
        mock_check_tables_exist.return_value = False
        records = [MagicMock(), MagicMock()]
        initDB(records)
        mock_initialize_schema.assert_called_once()
        mock_check_tables_exist.assert_called_once()
        mock_Session.assert_not_called()

    @patch("database.operations.check_tables_exist")
    @patch("database.operations.Session")
    def test_insertRow(self, mock_Session, mock_check_tables_exist):
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
    def test_insertRow_tables_not_exist(self, mock_Session, mock_check_tables_exist):
        mock_check_tables_exist.return_value = False
        row = MagicMock()
        insertRow(row)
        mock_Session.assert_not_called()

    @patch("database.operations.check_tables_exist")
    @patch("database.operations.Session")
    def test_insertRow_exception(self, mock_Session, mock_check_tables_exist):
        mock_check_tables_exist.return_value = True
        mock_session = MagicMock()
        mock_Session.return_value = mock_session
        mock_session.commit.side_effect = SQLAlchemyError()

        row = MagicMock()
        row.__tablename__ = "test_table"
        with self.assertRaises(SQLAlchemyError):
            insertRow(row)

    @patch("database.operations.MetaData")
    @patch("database.operations.Table")
    @patch("database.operations.engine")
    def test_initialize_schema(self, mock_engine, mock_Table, mock_MetaData):
        mock_metadata = MagicMock()
        mock_MetaData.return_value = mock_metadata

        initialize_schema()

        mock_MetaData.assert_called_once()
        self.assertEqual(mock_Table.call_count, 2)  # Called for both tables
        mock_metadata.create_all.assert_called_once_with(mock_engine)

    @patch("database.operations.MetaData")
    @patch("database.operations.engine")
    def test_initialize_schema_exception(self, mock_engine, mock_MetaData):
        mock_metadata = MagicMock()
        mock_MetaData.return_value = mock_metadata
        mock_metadata.create_all.side_effect = SQLAlchemyError()

        with self.assertRaises(SQLAlchemyError):
            initialize_schema()


class TestDatabaseSchema(unittest.TestCase):
    def test_AcademyAwardWinningFilms(self):
        film = AcademyAwardWinningFilms("test-id", "Test Film", 2020, 1, 5)
        self.assertEqual(film.id, "test-id")
        self.assertEqual(film.film, "Test Film")
        self.assertEqual(film.year, 2020)
        self.assertEqual(film.awards, 1)
        self.assertEqual(film.nominations, 5)

    def test_TestTable(self):
        test_entry = TestTable("test-id", "Test Entry")
        self.assertEqual(test_entry.id, "test-id")
        self.assertEqual(test_entry.text, "Test Entry")


class TestWikipediaUUID(unittest.TestCase):
    @patch("wiki.fetchPage")
    @patch("bs4.BeautifulSoup")
    def test_scrape_oscar_winning_films(self, mock_bs, mock_fetchPage):
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
        self.assertEqual(len(results), 1373)
        self.assertEqual(len(results[0]), 5)  # id, film, year, awards, nominations

    @patch("scripts.wikipedia_uuid.fetchPage")
    def test_scrape_oscar_winning_films_exception(self, mock_fetchPage):
        mock_fetchPage.return_value = None
        with self.assertRaises(Exception) as context:
            scrape_books()

        self.assertTrue("Failed to fetch the Wikipedia page" in str(context.exception))

    @patch("scripts.wikipedia_uuid.scrape_oscar_winning_films")
    @patch("scripts.wikipedia_uuid.initDB")
    @patch("scripts.wikipedia_uuid.insertRow")
    @patch("scripts.wikipedia_uuid.exportToCsv")
    @patch("scripts.wikipedia_uuid.exportToJson")
    def test_main(
        self,
        mock_exportToJson,
        mock_exportToCsv,
        mock_insertRow,
        mock_initDB,
        mock_scrape,
    ):
        mock_scrape.return_value = [
            ("id1", "Film 1", 2021, 1, 3),
            ("id2", "Film 2", 2022, 2, 5),
        ]
        main()
        mock_scrape.assert_called_once()
        mock_initDB.assert_called_once()
        self.assertEqual(mock_insertRow.call_count, 2)
        mock_exportToCsv.assert_called_once()
        mock_exportToJson.assert_called_once()


if __name__ == "__main__":
    unittest.main(
        testRunner=unittest.TextTestRunner(resultclass=WikiFilmDataTestResult)
    )
