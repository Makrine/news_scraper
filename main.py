from db_handler import fetch_articles
from text_processing import clean_text, clean_text_spacy, get_sentiment
from bbc_news_scraper import scrape_article_details

def main():

    url = 'https://www.bbc.com/'
    # scrape_article_details(url)

    query = "SELECT id, title, summary, tag, last_updated FROM articles"
    df = fetch_articles(query)

    if df is not None:
        # Apply text cleaning to the summary column using NLTK
        df['cleaned_summary_nltk'] = df['summary'].apply(clean_text)
        
        # Apply text cleaning to the summary column using SpaCy
        df['cleaned_summary_spacy'] = df['summary'].apply(clean_text_spacy)
        
        # Apply sentiment analysis
        df['sentiment'] = df['summary'].apply(get_sentiment)
        
        # Print the results
        print(df[['summary', 'cleaned_summary_nltk', 'cleaned_summary_spacy', 'sentiment']].head())

if __name__ == "__main__":  
    main()
