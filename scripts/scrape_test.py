# figuring out beautiful soup
import logging

from sbooks import BeautifulSoup as bs
from sbooks import fetchPage

###################################################################################################
#                                                                                                 #
#                                       Note from Finn                                            #
#                                                                                                 #
###################################################################################################
## Strategy 1: Category-based Approach                                                            #
###################################################################################################
### a. Parse the main page to extract all category links from the sidebar.                        #
### b. For each category, navigate to its page and extract book details                           #
### (title, price, availability, star rating) from the product pods.                              #
### c. Use pagination to iterate through all pages within each category,                          #
### repeating the extraction process.                                                             #
### d. Generate a UUID for each book and associate it with the current category.                  #
### e. Store the collected data (UUID, title, price, availability, star rating, category)         #
### in a structured format (e.g., list of dictionaries) for later processing.                     #
### f. Export to CSV, JSON and store in the database                                              #
###################################################################################################
## Strategy 2: Book-centric Approach                                                              #
###################################################################################################
### a. Start from the main page and extract basic book information                                #
### (title, price, availability, star rating) from the product pods.                              #
### b. For each book, follow its link to the detailed product page to extract additional          #
### information, including the category.                                                          #
### c. Generate a UUID for each book and associate it with all collected data.                    #
### d. Use pagination to navigate through all pages on the main site,                             #
### repeating steps 1-3 for each page.                                                            #
### e. Implement error handling and retry mechanisms to manage potential network issues           #
### or inconsistencies in the page structure.                                                     #
###################################################################################################

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
                category_name = a_tag.string.strip()
                print("category name: ",category_name)

                category_page = bs(fetchPage(url+category_link).content, features="html.parser")

                num_pages = 1
                num_pages_tag = category_page.find(class_="current")
                if(num_pages_tag is not None):
                    # print(num_pages_tag.text.split("of ",1)[1])

                    num_pages = int(num_pages_tag.text.split("of ",1)[1])

                if num_pages == 1:
                    print("stub")
                else:
                    for i in range(num_pages):
                        # page n is just page-n.html instead of index.html
                        new_page_url = category_link.replace("index", "page-"+i)
                        current_page = bs(fetchPage(url+new_page_url).content, features="html.parser")


        #return books
    except Exception as e:
        logging.error(f"Error scraping Oscar-winning films: {str(e)}")
        raise


scrape_books()
