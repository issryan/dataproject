import sqlite3
import json

# Full JSON data from your curl command
data_json = """
{
    "businesses": [
        {"name": "Scotiabank", "location": {"display_address": ["392 Bay St", "Toronto, ON M5H 3K5", "Canada"]}, "rating": 2.4},
        {"name": "Scotiabank", "location": {"display_address": ["992 Bloor Street W", "Toronto, ON M6H 1M1", "Canada"]}, "rating": 3.5},
        {"name": "Scotiabank", "location": {"display_address": ["720 King St W", "Toronto, ON M5V 2T3", "Canada"]}, "rating": 3.7},
        {"name": "Scotiabank", "location": {"display_address": ["555 Yonge Street", "Toronto, ON M4Y 3A6", "Canada"]}, "rating": 2.5},
        {"name": "Scotiabank", "location": {"display_address": ["292 Spadina Avenue", "Toronto, ON M5T 2E7", "Canada"]}, "rating": 2.2},
        {"name": "Scotiabank", "location": {"display_address": ["145 King St W", "Toronto, ON M5H 1J8", "Canada"]}, "rating": 2.3},
        {"name": "Scotiabank", "location": {"display_address": ["70 Carlton Street", "Toronto, ON M5B 1L6", "Canada"]}, "rating": 5.0},
        {"name": "Scotiabank", "location": {"display_address": ["410 Bathurst Street", "Unit 2A", "Toronto, ON M5T 2S6", "Canada"]}, "rating": 2.0},
        {"name": "Scotiabank", "location": {"display_address": ["222 Queen St W", "Toronto, ON M5V 1Z3", "Canada"]}, "rating": 2.0},
        {"name": "Scotiabank", "location": {"display_address": ["2200 Yonge St", "Toronto, ON M4S 2C6", "Canada"]}, "rating": 1.0},
        {"name": "Scotiabank", "location": {"display_address": ["40 King St W", "Toronto, ON M5H 3Y2", "Canada"]}, "rating": 2.0},
        {"name": "Scotiabank", "location": {"display_address": ["522 University Ave", "Toronto, ON M5G 1W7", "Canada"]}, "rating": 4.0},
        {"name": "Scotiabank", "location": {"display_address": ["643 College St", "Toronto, ON M6G 1B7", "Canada"]}, "rating": 2.0},
        {"name": "Scotiabank", "location": {"display_address": ["363 Broadview Avenue", "Toronto, ON M4K 2M7", "Canada"]}, "rating": 4.0},
        {"name": "Scotiabank", "location": {"display_address": ["41 Harbour Square", "Toronto, ON M5J 2G4", "Canada"]}, "rating": 3.0},
        {"name": "Scotiabank", "location": {"display_address": ["2295 Bloor St W", "Toronto, ON M6S 1P1", "Canada"]}, "rating": 3.5},
        {"name": "Scotiabank", "location": {"display_address": ["649 Danforth Avenue", "Toronto, ON M4K 1R2", "Canada"]}, "rating": 2.3},
        {"name": "Scotiabank", "location": {"display_address": ["1154 St Clair Avenue W", "Toronto, ON M6C 1C7", "Canada"]}, "rating": 3.0},
        {"name": "Scotiabank", "location": {"display_address": ["1046 Queen Street E", "Toronto, ON M4M 1K4", "Canada"]}, "rating": 1.3}
    ]
}
"""

# Parse the JSON
data = json.loads(data_json)

# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('scotiabank_branches.db')
c = conn.cursor()

# Create a table
c.execute('''
CREATE TABLE IF NOT EXISTS branches (
    address TEXT,
    rating REAL
)
''')

# Insert data into the table
for business in data['businesses']:
    address = ", ".join(business['location']['display_address'])
    rating = business['rating']
    c.execute('INSERT INTO branches (address, rating) VALUES (?, ?)', (address, rating))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into the database.")