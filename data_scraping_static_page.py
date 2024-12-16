import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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


def save_to_excel(data, filename="static_page.xlsx"):
    """
    Saves the article data (URL and HTML content) to an Excel file.

    Args:
    data (list of dict): List containing article data to be saved.
    filename (str): The name of the Excel file to save the data.
    """
    # Create a DataFrame from the list of data
    df = pd.DataFrame(data)

    # Write DataFrame to an Excel file
    df.to_excel(filename, index=False, engine='openpyxl')


# Example usage
if __name__ == "__main__":
    # Take a URL input
    article_url = input("Enter the news article URL: ")
    
    # Fetch the HTML content
    html_content = fetch_html(article_url)
    
    if html_content:
        print("Successfully retrieved the article's HTML content.")
        
        # Prepare the data to be saved (including the URL and the HTML content)
        article_data = {
            "URL": article_url,
            "HTML_Content": str(html_content.prettify()),
            "Date_Fetched": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save the data to Excel
        save_to_excel([article_data])
        print(f"Data has been successfully saved to Excel file.")
    else:
        print("Failed to retrieve article content.")
