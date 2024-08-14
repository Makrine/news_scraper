from db_handler import fetch_articles
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import spacy
from textblob import TextBlob

query = "SELECT id, title, summary, tag, last_updated FROM articles"
df = fetch_articles(query)

# Download stopwords if not already done
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

# Initialize stop words
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = word_tokenize(text.lower())
    # Remove stop words
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

nlp = spacy.load('en_core_web_sm')

def clean_text_spacy(text):
    # Process text
    doc = nlp(text)
    # Remove stop words and punctuation
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


if df is not None:
    # print(df.head())
    # Apply text cleaning to the summary column
    df['cleaned_summary'] = df['summary'].apply(clean_text)
    #print(df[['summary', 'cleaned_summary']].head())

    # Apply text cleaning to the summary column
    df['cleaned_summary'] = df['summary'].apply(clean_text_spacy)
    #print(df[['summary', 'cleaned_summary']].head())

    df['sentiment'] = df['summary'].apply(get_sentiment)
    print(df[['summary', 'summary', 'sentiment']].head())