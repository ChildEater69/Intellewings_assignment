import pymysql

# Establish connection to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='admin',
    db='article_data',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conn.cursor() as cursor:
        # Create table (if it doesn't exist)
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            content TEXT,
            date_scrapped DATE
        );
        '''
        cursor.execute(create_table_query)
        
        # Insert data into the table
        insert_query = '''
        INSERT INTO articles (title, content, date_scrapped)
        VALUES (%s, %s, %s)
        '''
        
        # Data to insert (example)
        data = [
            ("Article 1", "Content of article 1", "2024-12-15"),
            ("Article 2", "Content of article 2", "2024-12-16")
        ]
        
        # Execute insert query for each data entry
        cursor.executemany(insert_query, data)
        
        # Commit the changes to the database
        conn.commit()
        
        print("Data successfully inserted.")
        
finally:
    # Close the connection
    conn.close()
