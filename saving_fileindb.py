import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import spacy
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import pipeline
import pymysql

# Load the trained NER model
nlp = spacy.load("en_core_web_sm")

# Initialize DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')

# Initialize Hugging Face's sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Establish connection to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='admin',
    db='article_data',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()

# Create a table to store the article data within the 'scrapped_data' schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS scrapped_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url TEXT,
    extracted_person TEXT,
    extracted_org TEXT,
    sentiment_positive INT,
    sentiment_negative INT,
    date_fetched DATETIME
)
''')
conn.commit()

def fetch_html(url):
    """
    Takes a URL as input and retrieves the HTML content of the article.
    
    Args:
    url (str): The URL of the news article.

    Returns:
    str: The HTML content of the article.
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Return the HTML content
            return soup
        else:
            print(f"Failed to retrieve the article. HTTP Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_entities(text):
    """
    Extracts named entities from the given text using the NER model.
    
    Args:
    text (str): The text to extract entities from.

    Returns:
    dict: A dictionary containing comma-separated 'PERSON' and 'ORG' entities.
    """
    doc = nlp(text)
    entities = {"PERSON": [], "ORG": []}
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["PERSON"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["ORG"].append(ent.text)
    
    # Join the entities into comma-separated strings
    entities["PERSON"] = ', '.join(entities["PERSON"])
    entities["ORG"] = ', '.join(entities["ORG"])
            
    return entities

def analyze_sentiment_distilbert(text):
    """
    Analyzes the sentiment of the given text using DistilBERT.
    
    Args:
    text (str): The text to analyze.

    Returns:
    dict: A dictionary with counts of 'POSITIVE' and 'NEGATIVE' sentiments.
    """
    # Split the text into chunks
    chunk_size = 512
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    sentiments = {"POSITIVE": 0, "NEGATIVE": 0}
    for chunk in chunks:
        result = sentiment_pipeline(chunk)[0]
        sentiments[result['label']] += 1
    
    return sentiments

def store_data_in_db(data):
    """
    Stores the article data in the MySQL database.
    
    Args:
    data (dict): The article data to be stored.
    """
    try:
        sql = """
        INSERT INTO scrapped_data (url, extracted_person, extracted_org, sentiment_positive, sentiment_negative, date_fetched)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data["url"],
            data["extracted_person"],
            data["extracted_org"],
            data["sentiment_positive"],
            data["sentiment_negative"],
            data["date_fetched"]
        )

        cursor.execute(sql, values)
        conn.commit()

        print("Data has been successfully stored in the database.")
    except Exception as e:
        print(f"An error occurred while storing data: {e}")

# Example usage
if __name__ == "__main__":
    # Take a URL input
    article_url = input("Enter the news article URL: ")

    # Fetch the HTML content
    html_content = fetch_html(article_url)
    
    if html_content:
        print("Successfully retrieved the article's HTML content.")
        
        # Extract text content from HTML
        article_text = html_content.get_text(separator=' ', strip=True)
        
        # Extract entities from the article text
        entities = extract_entities(article_text)
        
        # Analyze sentiment of the article text using DistilBERT
        sentiment_distilbert = analyze_sentiment_distilbert(article_text)
        
        # Prepare the data to be saved (including the URL, extracted entities, and sentiment)
        article_data = {
            "url": article_url,
            "extracted_person": entities["PERSON"],  # Now stored as a comma-separated string
            "extracted_org": entities["ORG"],  # Now stored as a comma-separated string
            "sentiment_positive": sentiment_distilbert["POSITIVE"],
            "sentiment_negative": sentiment_distilbert["NEGATIVE"],
            "date_fetched": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Store the data in the database
        store_data_in_db(article_data)
        
        # Optionally, print out the data and plot the sentiment chart
        print("Stored data:", article_data)
