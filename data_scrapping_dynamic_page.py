from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Function to get the page content after dynamic loading
def fetch_html_with_selenium(url):
    # Set up the webdriver (this will automatically download and set up the latest driver)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Use headless mode (no UI)
    
    # Setup the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Open the URL
    driver.get(url)
    
    # Wait for the page to load (you can adjust this depending on your needs)
    time.sleep(5)  # Wait for 5 seconds to ensure JavaScript has loaded the content
    
    # Get the page HTML content
    page_html = driver.page_source
    
    # Close the browser
    driver.quit()
    
    return page_html

# Function to save content to Excel
def save_to_excel(data, filename='dynamic_page.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

# Prompt the user for the URL
article_url = input("Enter the news article URL: ")

# Get the HTML content of the page
html_content = fetch_html_with_selenium(article_url)

# Store the HTML content in a list (for DataFrame)
data = [{'HTML Content': html_content}]

# Save the data to Excel
save_to_excel(data)

print("HTML content saved to 'dynamic_page.xlsx'")
