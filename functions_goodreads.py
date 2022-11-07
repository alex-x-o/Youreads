import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def get_soup_from_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    return soup

def get_all_links(soup):
    links = []
    
    for link in soup.find_all('a'):
        links.append(link.get('href'))
        
    return links

def get_id_from_url(url):
    num = re.search("[0-9]+", url)
    start = num.span()[0]
    end = num.span()[1]
    id_gr = url[start:end]
    
    return id_gr

# can I use this to get columns, I mean I don't have to, but maybe
def get_all_books_soup(url):
    soup = get_soup_from_url(url)
    hyperlink = soup.find('a', string=re.compile("s bookshelves", re.I))
    dest = hyperlink.get('href')
    page = requests.get(urljoin(url, dest))
    soup_books = BeautifulSoup(page.content, 'html.parser')
    
    return [page.url, soup_books]

def get_url_base(url): # get_all_books
    id_gr = None
    url_base = "https://goodreads.com/review/list/"
    if re.search('author', url):
        url_author, book_soup = get_all_books_soup(url)
        id_gr = get_id_from_url(url_author)
        url_base = url_base + str(id_gr)
    else:
        id_gr = get_id_from_url(url)
        url_base = url_base + str(id_gr)
    return url_base

# do i need these with get_url_base_instead?
def get_read_url(url_base):
    return url_base + "?shelf=read"

def get_currently_reading_url(url_base):
    return url_base + "?shelf=currently-reading"

def get_want_to_read_url(url_base):
    return url_base + "?shelf=to-read"

def get_tables(url):
    soup = get_soup_from_url(url)
    tables = soup.find_all('table')
    
    return tables

# maybe not needed
def get_database_columns(url):
    tables = get_tables(url)
    
    on_click = tables[0].find('a').get('onclick')
    
    # make a list
    open_bracket = on_click.find('(')
    close_bracket = on_click.find(')')
    string_list = on_click[open_bracket+2:close_bracket-1]
    
    # modify list
    splitted = string_list.split(',')
    columns = [word[1:-1] for word in splitted]
    
    return columns

def get_num_of_pages(url):
    soup = get_soup_from_url(url)
    pages = soup.find('div', {'id': "reviewPagination"})
    pages_links = pages.find_all('a')
    
    last_page = pages_links[len(pages_links)-2]
    num_of_pages = last_page.get_text()
    
    return int(num_of_pages)

# maybe add some recursive=False to any find and find_all trhrough this .py
# TODO: fix rating - get number of stars through spans or get translation for start and do it that way, I think the later one is better option, but I am the Alex from the past, I know nothing
# also why some names didn't strip good and have \n on the back, oh it's because of the asterisk, remove it
def get_books_from_page(url, page=1):
    tables = get_tables(url + "&page=" + str(page))
    book_rows = tables[1].find_all('tr', {'id': re.compile("review")})
    stats = ['isbn13', 'cover', 'title', 'author', 'avg_rating', 'rating', 'num_ratings', 'num_pages', 'date_started', 'date_read', 'read_count', 'comments']
    books = []

    for row in book_rows:
        book_details = {} # make new function get_book_details
        for stat in stats:
            field = row.find('td', {'class': re.compile(stat)})
            value = field.find('div', {'class': "value"})
            
            if stat == 'cover':
                value = value.find('img').get('src')
            elif stat == 'comments':
                value = "https://goodreads.com" + value.find('a').get('href')
            elif stat == 'num_pages':
                value = (value.get_text())[:-2]
            else:
                value = value.get_text()
            book_details[stat] = value.strip()
        books.append(book_details)

    return books
    
# not used currently, but maybe it will be needed later, at least for reference
def get_default_shelves_links(url_base):
    soup_books = get_soup_from_url(url_base)
    user_shelves = soup_books.find_all('div', {'class': "userShelf"}, limit=3)
    default_shelves_links = []
    for user_shelf in user_shelves:
        href = user_shelf.find('a').get('href')
        default_shelves_links.append(urljoin(url_base, href))
        
    return default_shelves_links

if __name__ == '__main__':
    main()