from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(440, 220) # optional
driver.get('example/index.html')
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#render_ready")))
img = driver.get_screenshot_as_png()
img = Image.open(BytesIO(img))
cropped = img.crop((0,0,440,220))
cropped.save('image.png')

elem = driver.find_element_by_css_selector('#tweet_text')
print(elem.get_attribute('innerHTML'))
# driver.save_screenshot('screen.png') # save a screenshot to disk
