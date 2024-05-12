from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_place_ids_from_search(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    
    # Wait for the search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    
    # Scroll down to ensure all results are loaded (may require adjustment based on page)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Allow time for any lazy-loaded elements to appear

    # Find all links in the search results, assuming each bank branch is linked individually
    elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/maps/place/Scotiabank")]')
    place_ids = []
    for element in elements:
        href = element.get_attribute('href')
        if 'placeid=' in href:
            place_id = href.split('placeid=')[-1].split('&')[0]
            place_ids.append(place_id)
    
    driver.quit()
    return place_ids

# URL containing the list of locations
url = 'https://www.google.com/maps/search/scotiabank+in+toronto/@43.6573563,-79.4170186,14.28z?entry=ttu'
place_ids = get_place_ids_from_search(url)
print(place_ids)
