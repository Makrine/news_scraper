import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import spacy
from textblob import TextBlob

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')


# Initialize SpaCy model and NLTK stop words
nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """Clean text using NLTK."""
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def clean_text_spacy(text):
    """Clean text using SpaCy."""
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def get_sentiment(text):
    """Get sentiment polarity using TextBlob."""
    blob = TextBlob(text)
    return blob.sentiment.polarity
