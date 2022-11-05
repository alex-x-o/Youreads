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

def get_read(url_base):
    return url_base + "?shelf=read"

def get_currently_reading(url_base):
    return url_base + "?shelf=currently-reading"

def get_want_to_read(url_base):
    return url_base + "?shelf=to-read"

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