import sqlite3
import json

# Define the SQLite database name
DATABASE_NAME = 'faq.db'

# Define the JSON file containing the FAQs
JSON_FILE = 'faq.json'

def create_database():
    """Create the SQLite database and knowledge_base table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database and table created successfully in {DATABASE_NAME}!")

def load_data_from_json():
    """Load FAQs from the JSON file into the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Open and load the JSON file
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)

    # Insert data into the table
    for item in data:
        cursor.execute('INSERT INTO knowledge_base (question, answer) VALUES (?, ?)', 
                       (item['question'], item['answer']))

    conn.commit()
    conn.close()
    print(f"FAQs loaded successfully from {JSON_FILE} into {DATABASE_NAME}!")

if __name__ == "__main__":
    # Step 1: Create the database and table
    create_database()
    
    # Step 2: Load the JSON file into the database
    load_data_from_json()
