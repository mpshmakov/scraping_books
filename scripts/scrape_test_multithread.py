import concurrent.futures
import threading
import uuid

from tqdm import tqdm

from sbooks import BeautifulSoup as bs
from sbooks import fetchPage
from sbooks import logger

# 1) extract links of categories
#     1. extract number of pages for this category
#       1. extract links of books
#           1. add book to the dataframe with the respective category

# TODO:
# dynamically allocate workers - DONE
# tqdm - DONE
# loguru (implement using passing an additional -l argument when launching the script or just write down logs in a separate file)

# implement dataframe
# db implementations
# tests

pbar_category = tqdm(total=50) # TODO: ideally this number should be dynamic

url = "https://books.toscrape.com/"

def category_worker(category):

    books = []

    a_tag = category.find('a')

    if type(a_tag) is not int: # for some reason some of the results are -1
        category_url = a_tag.get('href')
        category_name = a_tag.string.strip()
        logger.info("category name: " + category_name)

        category_page = bs(fetchPage(url+category_url).content, features="html.parser")

        num_pages = 1
        num_pages_tag = category_page.find(class_="current")

        if(num_pages_tag is not None):
            logger.info("num_pages is not None")
            num_pages = int(num_pages_tag.text.split("of ",1)[1])
        logger.info("pages: ", str(num_pages))

        new_page_url = category_url
        for i in range(num_pages):
            iterator = i+1

            # page n is just page-n.html instead of index.html
            if (iterator != 1):
                new_page_url = category_url.replace("index", "page-"+str(iterator))
            logger.info("current category page url: " + url+new_page_url)
            current_page = bs(fetchPage(url+new_page_url).content, features="html.parser")

            # get links of books
            books_tag = current_page.find('ol')
            books_a_tags = books_tag.find_all('a', title=True)

            for book_a in books_a_tags:
                book_url = book_a.get('href').split("/", 3)[3]
                logger.info("current book url: " + book_url)

                # soup of the book -> parse the details into a dict 
                book_page = bs(fetchPage(url+"catalogue/"+book_url).content, features="html.parser")
                main_div_tag = book_page.find(class_="col-sm-6 product_main")

                id = str(uuid.uuid4())
                logger.info("uuid: " + id)

                title = get_title(main_div_tag)
                logger.info("title: " + title)

                price = get_price(main_div_tag)
                logger.info("price: " + str(price))

                availability = get_availability(main_div_tag)
                logger.info("availability: " + str(availability))
                
                rating = get_rating(main_div_tag)
                logger.info("rating: " + str(rating))

                the_category = category_name
                logger.info("category: "+category_name)
                books.append([id, title, price, availability, rating, the_category])
    else:
        return

    pbar_category.update(1)
    return books

def word_number_to_int(number):
    if number == "One":
        return 1
    if number == "Two":
        return 2
    if number == "Three":
        return 3
    if number == "Four":
        return 4
    if number == "Five":
        return 5

# functions to get each of the books' parameters (i believe it is easier to debug and maintain the code this way because the parsing of the page may get very complicated)
def get_title(main_div_tag):
    title = main_div_tag.find('h1').text.strip()
    return title

def get_price(main_div_tag):
    price = main_div_tag.find(class_="price_color").text.strip()
    return price 

def get_availability(main_div_tag):
    tmp_availability = main_div_tag.find(class_="instock availability").text.strip().split("(",1)[1]
    availability = tmp_availability.split("available",1)[0]
    return availability

def get_rating(main_div_tag):
    tmp_star_rating = main_div_tag.find(class_="star-rating").get('class')[1]
    star_rating = word_number_to_int(tmp_star_rating)
    return star_rating


def scrape_books():

    books = []

    try:
        response = fetchPage(url)
        if response is None:
            raise Exception("Failed to fetch the Books page")

        soup = bs(response.content, features="html.parser")
        logger.info("Created the soup.")

        categories = soup.find(class_="nav nav-list").find('ul')

        categories_list = []

        for category in categories:
            categories_list.append(category)

        # removed max_workers. https://docs.python.org/3/library/concurrent.futures.html#:~:text=Changed%20in%20version%203.5%3A%20If,number%20of%20workers%20for%20ProcessPoolExecutor.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            books_map = executor.map(category_worker, categories_list)
            logger.debug("max workers: ", str(executor._max_workers)) 
        pbar_category.close()

        for book in books_map:
            if book != None:
                for j in range(len(book)):
                    books.append(book[j])
        

        return books
    except Exception as e:
        logger.error(f"Error scraping books: {str(e)}")
        raise


b = scrape_books()
logger.info("total books acquired: "+str(len(b)))