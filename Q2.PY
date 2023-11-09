import requests
from bs4 import BeautifulSoup
import csv
import re

# Constants
url = 'https://www.bookdepository.com/s/?category=all&field=keyword&listtype=0010&bookgroup=2567701'
book_title_selector = '.title a'
author_name_selector = '.author a'
author_contact_selector = '.publisher'

def get_page_count():
    page_count = 0
    while True:
        page_url = url + f'&page={page_count}'
        page_html = requests.get(page_url).text
        page_soup = BeautifulSoup(page_html, 'html.parser')
        page_link = page_soup.find('li', {'class': 'selected'}).find_next_sibling('li').find('a')
        if not page_link:
            break
        page_count += 1
    return page_count

def scrape_books(page_count):
    book_details = []
    for i in range(page_count):
        page_url = url + f'&page={i}'
        page_html = requests.get(page_url).text
        page_soup = BeautifulSoup(page_html, 'html.parser')
        book_containers = page_soup.find_all('div', {'class': 'grid-book-card'})
        for container in book_containers:
            book_title = container.find(book_title_selector).text
            author_name = container.find(author_name_selector).text
            author_contact = container.find(author_contact_selector).text
            book_details.append([book_title, author_name, author_contact])
    return book_details

def save_to_csv(book_details):
    with open('books.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Book Title', 'Author Name', 'Author Contact'])
        writer.writerows(book_details)

def main():
    page_count = get_page_count()
    book_details = scrape_books(page_count)
    save_to_csv(book_details)

if __name__ == '__main__':
    main()
