import json
import sqlite3

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['businesses']  

def save_to_database(data):
    conn = sqlite3.connect('scotiabank_branches.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS branches (
        address TEXT,
        rating REAL
    )
    ''')
    for item in data:
        address = ', '.join(item['location']['display_address']) if 'location' in item and 'display_address' in item['location'] else 'No Address'
        rating = item.get('rating', 0)  # Default rating to 0 if not found
        c.execute('INSERT INTO branches (address, rating) VALUES (?, ?)', (address, rating))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    json_file_path = 'yelp_scotia_data.json' 
    scraped_data = load_json_data(json_file_path)
    save_to_database(scraped_data)
    print("Data inserted successfully into the database.")