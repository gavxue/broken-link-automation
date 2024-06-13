from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://uwaterloo.ca/civil-environmental-engineering-information-technology")


def page():
    body = driver.find_element(By.TAG_NAME, 'main')
    links = body.find_elements(By.TAG_NAME, 'a')

    for link in links:
        link.click()
        driver.back()

    print(links)

def main():
    nav = driver.find_elements(By.TAG_NAME, "nav")
    nav_items = nav[2].find_elements(By.XPATH, './div/div/ul/li/a')

    for nav_item in nav_items:
        nav_item.click()
        if not 'menu__link-sub' in nav_item.get_attribute('class'):
            driver.back()
        

if __name__ == '__main__':
    main()