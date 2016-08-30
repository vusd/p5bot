from selenium import webdriver
from PIL import Image
from io import BytesIO

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(440, 220) # optional
driver.get('example/index.html')
img = driver.get_screenshot_as_png()
img = Image.open(BytesIO(img))
cropped = img.crop((0,0,440,220))
cropped.save('image.png')

elem = driver.find_element_by_css_selector('#tweet_text')
print(elem.get_attribute('innerHTML'))
# driver.save_screenshot('screen.png') # save a screenshot to disk
