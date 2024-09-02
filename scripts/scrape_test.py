# figuring out beautiful soup
import logging

from sbooks import BeautifulSoup as bs
from sbooks import fetchPage

# 1) extract links of categories
#     1. extract links of books
#     2. add books to the dataframe with the respective category

url = "https://books.toscrape.com/"


def scrape_books():
    try:
        response = fetchPage(url)
        if response is None:
            raise Exception("Failed to fetch the Books page")

        soup = bs(response.content, features="html.parser")
        logging.info("Created the soup.")

        categories = soup.find_all()

        return books
    except Exception as e:
        logging.error(f"Error scraping Oscar-winning films: {str(e)}")
        raise
