from db_handler import fetch_articles
from text_processing import clean_text_spacy, get_sentiment
import matplotlib.pyplot as plt
import seaborn as sns
from db_handler import delete_articles
from bbc_news_scraper import scrape_article_details

def plot_sentiment_distribution(df):
    """Plot the distribution of sentiment scores."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df['sentiment'], bins=30, kde=True, color='blue')
    plt.title('Sentiment Score Distribution')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    url = 'https://www.bbc.com/'
    
    # Scrape article details from the given URL
    scrape_article_details(url)

    query = "SELECT id, title, summary, tag, last_updated FROM articles"
    df = fetch_articles(query)

    if df is not None:
        # Apply text cleaning to the summary column using SpaCy
        df['cleaned_summary_spacy'] = df['summary'].apply(clean_text_spacy)
        
        # Apply sentiment analysis
        df['sentiment'] = df['summary'].apply(get_sentiment)
        
        # Print the results
        print(df[['summary', 'cleaned_summary_spacy', 'sentiment']].head())
        
        # Plot sentiment distribution
        plot_sentiment_distribution(df)

if __name__ == "__main__":
    main()
