import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

base_url = 'http://quotes.toscrape.com'
quotes_url = f'{base_url}/page/{{}}/'
authors = {}
quotes = []

def scrape_quotes(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote_block in soup.select('.quote'):
        text = quote_block.select_one('.text').get_text(strip=True)
        author = quote_block.select_one('.author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_block.select('.tag')]

        quotes.append({
            'tags': tags,
            'author': author,
            'quote': text
        })

        if author not in authors:
            author_url = base_url + quote_block.select_one('a')['href']
            scrape_author(author_url)

def scrape_author(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    fullname = soup.select_one('.author-title').get_text(strip=True)
    born_date = soup.select_one('.author-born-date').get_text(strip=True)
    born_location = soup.select_one('.author-born-location').get_text(strip=True)
    description = soup.select_one('.author-description').get_text(strip=True)

    authors[fullname] = {
        'fullname': fullname,
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    }

page = 1
while True:
    page_url = quotes_url.format(page)
    response = requests.get(page_url)
    if "No quotes found!" in response.text:
        break
    scrape_quotes(page_url)
    page += 1

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(list(authors.values()), f, ensure_ascii=False, indent=4)

client = MongoClient("mongodb+srv://maei86957:b.Susan1997@cluster0.ckmph.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['myDatabase']

with open('C:\\Users\\Marry\\Desktop\\Data_Science\\Module_3\\authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)
    db.authors.insert_many(authors_data)

with open('C:\\Users\\Marry\\Desktop\\Data_Science\\Module_3\\quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)
    db.quotes.insert_many(quotes_data)

print("Data imported successfully!")
