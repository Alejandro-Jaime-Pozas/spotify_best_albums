from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "https://www.rollingstone.com/music/music-lists/50-best-albums-of-2016-119690/"

# Replace 'path_to_webdriver' with the actual path to your WebDriver executable (e.g., chromedriver)
driver = webdriver.Chrome('c:\Program Files (x86)\chromedriver.exe')
driver.get(url)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(5)

# body_element = driver.find_element_by_tag_name('body')
# body_element.send_keys(Keys.CONTROL, 'a')
# time.sleep(1)  # Add a short delay to make sure the selection is completed
# copied_text = body_element.text

copied_text = driver.execute_script("return document.body.textContent;")

print(copied_text)

driver.quit()