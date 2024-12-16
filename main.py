from ner_and_save import process_article

if __name__ == "__main__":
    # Take a URL input
    article_url = input("Enter the news article URL: ")

    # Process the article (fetch, extract entities, and save to Excel)
    process_article(article_url)
