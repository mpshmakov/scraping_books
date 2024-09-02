"""
Books to Scrape scraper and database population script.
This script scrapes book data from the Books to Scrape website,
stores it in a database, and exports it to CSV and JSON formats.
"""

import logging
import uuid

import pandas as pd
from database import AcademyAwardWinningFilms, Session, TestTable, initDB, insertRow
from database.operations import check_tables_exist, initialize_schema
from sbooks import BeautifulSoup as bs
from sbooks import fetchPage, requests
from sbooks.export_functions import exportToCsv, exportToJson
from sbooks.utils import clean_numeric
from sqlalchemy.exc import SQLAlchemyError


def scrape_books():
    """
    Scrape books data from https://books.toscrape.com/.
    Returns:
    list: A list of tuples containing books data (id, title, how many in stock, rating, category).
    Raises:
    Exception: If the page structure has changed and data cannot be scraped.
    """
    url = "https://books.toscrape.com/"
    try:
        response = fetchPage(url)
        if response is None:
            raise Exception("Failed to fetch the Books page")

        soup = bs(response.content, features="html.parser")
        logging.info("Created the soup.")

        table = soup.find("table", class_="wikitable")
        if not table:
            raise Exception("Unable to find the wikitable on the page.")

        trs = table.find("tbody").find_all("tr")
        logging.info("Successfully found elements in the soup.")

        movies = []
        for tr in trs[1:]:  # Skip the header row
            tds = tr.find_all("td")
            if len(tds) >= 4:  # Ensure the row has enough columns
                id = str(uuid.uuid4())
                film = tds[0].text.strip()
                year = clean_numeric(tds[1].text.strip())
                awards = clean_numeric(tds[2].text.strip())
                nominations = clean_numeric(tds[3].text.strip())
                movies.append((id, film, year, awards, nominations))
            else:
                logging.warning("Didn't manage to find 4 necessary columns in the row.")

        if not movies:
            raise Exception("No movie data was scraped from the page.")

        return movies
    except Exception as e:
        logging.error(f"Error scraping Oscar-winning films: {str(e)}")
        raise


def main():
    """
    Main function to orchestrate the scraping, database population, and data export process.
    """
    try:

        # Initialize the database schema
        initialize_schema()

        # Verify tables exist
        if not check_tables_exist():
            logging.error("Tables do not exist after schema initialization. Exiting.")
            return

        movies_data = scrape_books()

        # Create AcademyAwardWinningFilms objects
        movies = [AcademyAwardWinningFilms(*movie) for movie in movies_data]

        # Initialize the database and insert all movies
        initDB(movies)

        # Verify tables exist again
        if not check_tables_exist():
            logging.error("Tables do not exist after initDB. Exiting.")
            return

        # Test inserting individual rows
        new_film = AcademyAwardWinningFilms(str(uuid.uuid4()), "Test Film", 2023, 1, 5)
        new_test = TestTable(str(uuid.uuid4()), "Test entry")
        insertRow(new_film)
        print("Inserted new film.")
        insertRow(new_test)
        print("Inserted test entry.")

        # Create DataFrame for CSV and JSON export
        df = pd.DataFrame(
            movies_data, columns=["id", "film", "year", "awards", "nominations"]
        )
        exportToCsv(df)
        exportToJson(df)
        print("CSV and JSON files created successfully.")

    except SQLAlchemyError as e:
        logging.error(f"A database error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
