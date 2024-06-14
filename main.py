from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://uwaterloo.ca/civil-environmental-engineering-information-technology")


def page():
    body = driver.find_element(By.TAG_NAME, 'main')
    links = body.find_elements(By.TAG_NAME, 'a')

    for link in links:
        link.click()
        driver.back()

    print(links)

def submenu(subnav):
    subnav_items = subnav.find_elements(By.XPATH, '../ul/li/a')
    
    for subnav_item in subnav_items:
        # print(subnav_item.get_attribute('class'))
        li = subnav_item.find_element(By.XPATH, '..')
        print(li.get_attribute('class'))
        if 'has-submenu' in li.get_attribute('class'):    
            print('skip')
        else:
            subnav_item.click()
            driver.back()
            subnav.click()
            time.sleep(1)


def menu():
    nav = driver.find_elements(By.TAG_NAME, "nav")
    nav_main = nav[2]
    nav_items = nav_main.find_elements(By.XPATH, './div/div/ul/li/a')

    # navigates through menu
    for nav_item in nav_items:
        if 'menu__link-sub' in nav_item.get_attribute('class'):
            nav_item.click()
            submenu(nav_item)
        else:
            nav_item.click()
            # page()
            driver.back()
        

if __name__ == '__main__':
    menu()