import spacy
from data_scraping_static_page import fetch_html, save_to_excel
from datetime import datetime
import pandas as pd


# Load SpaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extracts named entities (persons and organizations) from a given text.
    
    Args:
    text (str): The article text.
    
    Returns:
    dict: A dictionary containing lists of persons and organizations.
    """
    # Process the text through the SpaCy model
    doc = nlp(text)

    # Extract entities classified as PERSON or ORG
    persons = []
    organizations = []
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            persons.append(ent.text)
        elif ent.label_ == "ORG":
            organizations.append(ent.text)

    return {
        "Persons": persons,
        "Organizations": organizations
    }

def process_article(url):
    """
    Fetches the HTML content of an article, extracts named entities,
    and saves the result to an Excel file.
    
    Args:
    url (str): The URL of the article to process.
    """
    # Fetch the HTML content from the URL
    html_content = fetch_html(url)

    if html_content:
        print("Successfully retrieved the article's HTML content.")
        
        # Extract the text from the HTML content
        article_text = html_content.get_text()

        # Extract named entities from the article text
        entities = extract_entities(article_text)

        # Prepare data to be saved to Excel for scraping results
        article_data = {
            "URL": url,
            "Persons": ", ".join(entities["Persons"]),
            "Organizations": ", ".join(entities["Organizations"]),
            "Date_Fetched": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save the scraping data to the static_page.xlsx file
        save_to_excel([article_data])

        # Prepare data for NER results (persons and organizations)
        ner_data = {
            "URL": url,
            "Persons": ", ".join(entities["Persons"]),
            "Organizations": ", ".join(entities["Organizations"]),
            "Date_Fetched": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save the NER results to a new Excel file with columns
        save_ner_to_excel([ner_data])
        print(f"Data has been successfully saved to static_page.xlsx and ner_results.xlsx.")
    else:
        print("Failed to retrieve article content.")

def save_ner_to_excel(data, filename="ner_results.xlsx"):
    """
    Saves the NER results (Persons and Organizations) to a new Excel file.
    
    Args:
    data (list of dict): List containing NER data to be saved.
    filename (str): The name of the Excel file to save the NER data.
    """
    # Create a DataFrame from the list of NER data
    df = pd.DataFrame(data)

    # Write DataFrame to an Excel file, ensuring data is saved in columns
    df.to_excel(filename, index=False, engine='openpyxl')
