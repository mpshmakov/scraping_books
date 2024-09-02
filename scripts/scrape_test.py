# figuring out beautiful soup
import logging

from sbooks import BeautifulSoup as bs
from sbooks import fetchPage

# 1) extract links of categories
#     1. extract links of books
#     2. extract number of pages for this category
#       1. add books to the dataframe with the respective category

url = "https://books.toscrape.com/"


def scrape_books():
    try:
        response = fetchPage(url)
        if response is None:
            raise Exception("Failed to fetch the Books page")

        soup = bs(response.content, features="html.parser")
        logging.info("Created the soup.")

        categories = soup.find(class_="nav nav-list").find('ul')

        
        for category in categories:
            a_tag = category.find('a')

            if type(a_tag) is not int: # for some reason some of the results are -1
                category_link = a_tag.get('href')
                category_name = category
        
                category_page = bs(fetchPage(url+category_link).content, features="html.parser")

                num_pages = 1
                num_pages_tag = category_page.find(class_="current")
                if(num_pages_tag is not None):
                    print(num_pages_tag.text.split("of ",1)[1])

                    num_pages = int(num_pages_tag.text.split("of ",1)[1])
                    
                    
                for i in range(num_pages):
                    # page n is just page-n.html instead of index.html
                    pritn('stub')
            
       
        #return books
    except Exception as e:
        logging.error(f"Error scraping Oscar-winning films: {str(e)}")
        raise


scrape_books()