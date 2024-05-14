import requests
import sqlite3

def fetch_and_save_business_info():
    # Define your Yelp API key here
    api_key = 'Your_Yelp_API_Key'
    headers = {'Authorization': f'Bearer {api_key}'}
    url = 'EAo83n9kjSHy7jMaUKF6RJxtKLvCeqBN3g1uSmD-XjTeIsWpI_mKkSWutO6EXt5OZ9q2uiZv6tyQzIqEs7VwroESEFAzSyz_3FkeRe2y5XXCCv8oUpESN4b9FM1CZnYx'

    # Set search parameters to focus on Scotiabank in Toronto
    params = {
        'term': 'Scotiabank',
        'location': 'Toronto',
        'limit': 50  # The maximum number of results per API call
    }

    # Make a request to the Yelp API
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        businesses = response.json().get('businesses', [])
        
        # Connect to SQLite Database
        conn = sqlite3.connect('scotiabank_branches.db')
        c = conn.cursor()
        
        # Create table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS branches (
                name TEXT,
                address TEXT,
                rating REAL
            )
        ''')

        # Insert data into the database
        for business in businesses:
            name = business['name']
            address = ", ".join(business['location']['display_address'])  # Join address parts
            rating = business['rating']
            c.execute('INSERT INTO branches (name, address, rating) VALUES (?, ?, ?)', (name, address, rating))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        print("Data fetched and saved to database successfully.")
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")

# Run the function
fetch_and_save_business_info()