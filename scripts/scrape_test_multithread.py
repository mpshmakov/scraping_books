import concurrent.futures
import logging
import uuid

from sbooks import BeautifulSoup as bs
from sbooks import fetchPage

# 1) extract links of categories
#     1. extract links of books
#     2. extract number of pages for this category
#       1. extract links of books
#           1. add book to the dataframe with the respective category

# TODO:
# dynamically allocate workers 
# loguru, tqdm
# db implementations
# tests


url = "https://books.toscrape.com/"

def category_worker(category):
    books = []

    a_tag = category.find('a')

    if type(a_tag) is not int: # for some reason some of the results are -1
        category_url = a_tag.get('href')
        category_name = a_tag.string.strip()
        print("category name: ",category_name)

        category_page = bs(fetchPage(url+category_url).content, features="html.parser")

        num_pages = 1
        num_pages_tag = category_page.find(class_="current")

        if(num_pages_tag is not None):
            print("num_pages is not None")
            num_pages = int(num_pages_tag.text.split("of ",1)[1])
        print("pages: ", num_pages)

        new_page_url = category_url
        for i in range(num_pages):
            iterator = i+1

            # page n is just page-n.html instead of index.html
            if (iterator != 1):
                new_page_url = category_url.replace("index", "page-"+str(iterator))
            print("current url: ", url+new_page_url)
            current_page = bs(fetchPage(url+new_page_url).content, features="html.parser")

            # get links of books
            books_tag = current_page.find('ol')
            books_a_tags = books_tag.find_all('a', title=True)
            
            for book_a in books_a_tags:
                book_url = book_a.get('href').split("/", 3)[3]
                print("book_url", book_url)

                # soup of the book -> parse the details into a dict 
                print("\nfound: ")

                book_page = bs(fetchPage(url+"catalogue/"+book_url).content, features="html.parser")
                main_div_tag = book_page.find(class_="col-sm-6 product_main")

                id = str(uuid.uuid4())
                title = get_title(main_div_tag)
                price = get_price(main_div_tag)
                availability = get_availability(main_div_tag)
                rating = get_rating(main_div_tag)
                the_category = category_name
                books.append([id, title, price, availability, rating, the_category])
                print("\n")
    else:
        return

    print("total books", len(books))
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
    print("title: ", title)
    return title

def get_price(main_div_tag):
    price = main_div_tag.find(class_="price_color").text.strip()
    print("price: ", price)
    return price 

def get_availability(main_div_tag):
    tmp_availability = main_div_tag.find(class_="instock availability").text.strip().split("(",1)[1]
    availability = tmp_availability.split("available",1)[0]
    print("availability: ", availability)
    return availability

def get_rating(main_div_tag):
    tmp_star_rating = main_div_tag.find(class_="star-rating").get('class')[1]
    star_rating = word_number_to_int(tmp_star_rating)
    print("stars: ", star_rating)
    return star_rating


def scrape_books():

    books = []

    try:
        response = fetchPage(url)
        if response is None:
            raise Exception("Failed to fetch the Books page")

        soup = bs(response.content, features="html.parser")
        logging.info("Created the soup.")

        categories = soup.find(class_="nav nav-list").find('ul')

        categories_list = []

        for category in categories:
            categories_list.append(category)

        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
            books_map = executor.map(category_worker, categories_list)
        
        for book in books_map:
            if book != None:
                print(book)
                for j in range(len(book)):
                    books.append(book[j])

        return books
    except Exception as e:
        logging.error(f"Error scraping books: {str(e)}")
        raise


b = scrape_books()
print(len(b))
