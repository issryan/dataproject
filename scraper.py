from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sqlite3

def scrape_branch_info():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-dev-shm-usage')  
    chrome_options.add_argument('--headless')  

    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.google.com/maps/search/Scotiabank+in+Toronto"
    driver.get(url)
    time.sleep(5)  

    branches = []
    try:
        # Scroll to load all elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Assuming the addresses and reviews are within elements with specific classes
        results = driver.find_elements(By.CLASS_NAME, 'section-result')
        for result in results:
            # Use try-except to catch and print any errors encountered per branch
            try:
                name = result.find_element(By.CLASS_NAME, 'section-result-title').text
                address = result.find_element(By.CLASS_NAME, 'section-result-location').text
                rating = result.find_element(By.CLASS_NAME, 'cards-rating-score').text
                branches.append((name, address, rating))
                print(f"Scraped: {name}, {address}, {rating}")  
            except Exception as e:
                print(f"Error scraping a branch: {e}")

    finally:
        driver.quit()
    return branches

def save_to_sqlite(data):
    print(f"Data to insert: {data}")  
    conn = sqlite3.connect('scotiabank_branches.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            name TEXT,
            address TEXT,
            rating TEXT
        )
    ''')
    c.executemany('INSERT INTO branches (name, address, rating) VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()
    print("Data insertion complete.")  

# Run the function and print the results
branch_data = scrape_branch_info()
save_to_sqlite(branch_data)
