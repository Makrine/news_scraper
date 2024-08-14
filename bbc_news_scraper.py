import requests
from bs4 import BeautifulSoup
from db_handler import insert_article
import logging
from time import sleep
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_article_details(url):
    """Scrape article details from the given URL and store them in the database."""
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)  # Added timeout for request
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all parent divs with data-testid="edinburgh-article"
                articles = soup.find_all('div', attrs={"data-testid": "edinburgh-article"})
                
                if not articles:
                    logging.info("No articles found.")
                
                for idx, article in enumerate(articles):
                    headline = extract_text(article, "card-headline", "No headline found")
                    summary = extract_text(article, "card-description", "No summary found")
                    last_updated = extract_text(article, "card-metadata-lastupdated", "No last updated info found")
                    tag = extract_text(article, "card-metadata-tag", "No tag found")

                    logging.info(f"Article {idx + 1}: Headline: {headline}, Last Updated: {last_updated}, Tag: {tag}, Summary: {summary}")

                    insert_article(headline, summary, last_updated, tag)

                break  # Exit loop if request is successful

            else:
                logging.warning(f"Failed to retrieve the page. Status code: {response.status_code}")
                sleep(random.uniform(1, 3))  # Random sleep before retry

        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            sleep(random.uniform(1, 3))  # Random sleep before retry

def extract_text(article, data_testid, default_text):
    """Helper function to extract text from article based on data-testid attribute."""
    element = article.find(attrs={"data-testid": data_testid})
    return element.get_text(strip=True) if element else default_text
