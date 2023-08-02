from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "YOUR_WEBPAGE_URL_HERE"

# Replace 'path_to_webdriver' with the actual path to your WebDriver executable (e.g., chromedriver)
driver = webdriver.Chrome(executable_path='path_to_webdriver')
driver.get(url)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(5)

body_element = driver.find_element_by_tag_name('body')
body_element.send_keys(Keys.CONTROL, 'a')
time.sleep(1)  # Add a short delay to make sure the selection is completed
copied_text = body_element.text

print(copied_text)

driver.quit()