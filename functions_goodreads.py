import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import numpy as np

s = requests.Session()

def get_soup_from_url(url):
    global s
    while(True):
        page = s.get(url, headers={'X-Requested-With':'XMLHttpRequest'})
        cookies = s.cookies.get_dict()
        if cookies.get('srb_8') is None or cookies['srb_8'] == '0_ar': # if there's no cookies with this name or if it has this desired value then stop looking further
            break
        s = requests.Session()
    soup = BeautifulSoup(page.text, 'lxml')
    
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
    page_url = urljoin(url, dest)
    soup_books = get_soup_from_url(page_url)
    
    return [page_url, soup_books]

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
    
    if pages is None:
        return 1
    
    pages_links = pages.find_all('a')
    
    last_page = pages_links[len(pages_links)-2]
    num_of_pages = last_page.get_text()
    
    return int(num_of_pages)

# 12 out of 30
stats = ['cover', 'title', 'author', 'avg_rating', 'rating', 'num_ratings', 'num_pages', 'date_started', 'date_read', 'read_count', 'format', 'actions']

# everything is str, later will be changed to appropriate types in pd
translate_rating = {
    'did not like it': '1',
    'it was ok': '2',
    'liked it':'3',
    'really liked it': '4',
    'it was amazing': '5'
}

# 3/11/2000 best format option because of the argument infer_datetime_format=True for speeding up

translate_month = {
    'Jan': '1',
    'Feb': '2',
    'Mar': '3',
    'Apr': '4',
    'May': '5',
    'Jun': '6',
    'Jul': '7',
    'Aug': '8',
    'Sep': '9',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

def get_genres(book_url):
    soup_book = get_soup_from_url(book_url)
    
    genres = []
    links = soup_book.body.findAll('a', {'href': re.compile(r'/genres/')})
    for link in links:
        genre = link.span.get_text()
        genres.extend([genre])
    
    if len(genres) > 1:
        return genres
    else:
        return None
    
def remove_commas(value):
    
    while(True):
        comma = value.find(',')
        if comma == -1:
            break
        value = value[0:comma] + value[comma+1:len(value)]
        
    return value

def format_book_details(stat, value):
    if stat == 'cover':
        value = value.find('img').get('src')
    elif stat == 'comments':
        value = "https://goodreads.com" + value.find('a').get('href')
    elif stat == 'actions':
        value = value.find('a')
        if value.text.find('(with text)') == -1:
            value = ''
        else:
            value = "https://goodreads.com" + value.get('href')
    elif stat == 'num_pages':
        value = value.get_text()
        pp = value.find('pp')
        value = value[:pp].strip()
        if value == 'unknown':
            value = ''
        else:
            value = remove_commas(value)
    elif stat == 'rating':
        value = value.find('span')
        if value.get('title'):
            value = translate_rating[value.get('title')]
        else:
            value = ''
    elif stat == 'author':
        value = value.get_text()
        if re.search(r'/*', value):
            asterisk = value.find('*')
            value = value[:asterisk]
        value = value.strip()
    elif stat == 'date_started' or stat == 'date_read':
        value = value.find('div', {'class': 'date_row'}) # I will only look the last/first reading dates
        value = value.get_text().strip()
        comma = value.find(',')
        if comma == -1: # if format is month year than it's gonna be NaN
            value = ''
        else:
            value = value[0:comma] + value[comma+1:len(value)]
            month_day_year = value.split(' ')
            month = month_day_year[0].strip()
            day = month_day_year[1].strip()
            year = month_day_year[2].strip()
            month = translate_month[month]
            value = day + '/' + month + '/' + year
    elif stat == 'num_ratings':
        value = value.get_text().strip()
        value = remove_commas(value)
    else:
        value = value.get_text().strip()
        
    return value

def get_book_details(book_row):
    book_details = {}
    
    for stat in stats:
        field = book_row.find('td', {'class': stat})
        value = field.find('div', {'class': "value"})
        
        value = format_book_details(stat, value)
        
        # is string empty
        if value == '':
            book_details[stat] = np.nan
        else:
            book_details[stat] = value
    
    book_url = "https://goodreads.com" + book_row.find('a').get('href')
    book_details['book_url'] = book_url
    book_details['genres'] = get_genres(book_url)
        
    return book_details

# maybe add some recursive=False to any find and find_all trhrough this .py
# maybe change virtual env and update python to 3.10 so I can use match case instead of this stupid elif's
def get_books_from_page(url, page=1):
    tables = get_tables(url + "&page=" + str(page))
    book_rows = tables[1].find_all('tr', {'id': re.compile("review")})
    
    books = []

    for book_row in book_rows:
        book_details = get_book_details(book_row)
        books.append(book_details)

    return books

# shelf is also url/url_base
def get_books_from_shelf(shelf):
    num_of_pages = get_num_of_pages(shelf)
    
    all_books = []
    for i in range(1, num_of_pages+1):
        book_page = get_books_from_page(shelf, i)
        all_books.extend(book_page)

    return all_books

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