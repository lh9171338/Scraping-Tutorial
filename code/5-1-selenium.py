from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


service = Service('../chromedriver.exe')
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

# add the option when creating driver
driver.get("https://mofanpy.com/")
driver.find_element(By.XPATH, "//img[@alt='强化学习 (Reinforcement Learning)']").click()
driver.find_element(By.LINK_TEXT, 'About').click()
driver.find_element(By.LINK_TEXT, '赞助').click()
driver.find_element(By.LINK_TEXT, '学习 ▾').click()
driver.find_element(By.LINK_TEXT, '数据处理 ▾').click()
driver.find_element(By.LINK_TEXT, '网页爬虫').click()

print(driver.page_source[:200])
driver.get_screenshot_as_file("../image/sreenshot2.png")
driver.close()
print('finish')
