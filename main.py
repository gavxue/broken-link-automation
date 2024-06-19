from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
from colored import fore, back, style

url = "https://uwaterloo.ca/civil-environmental-engineering-information-technology"

driver = webdriver.Chrome()
driver.get(url)

broken_links = 0

# colours
color_success = f"{fore('green')}"
color_error = f"{fore('red')}"
color_warning = f"{fore('yellow')}"
color_menu = f"{style('bold')}{fore('magenta')}{back('yellow')}"
color_submenu = f"{style('bold')}{fore('blue')}"
color_prompt = f"{fore('cyan')}"


def pause():
    time.sleep(0.1)


def check_status(link):
    global broken_links

    text = link.text
    status = "HTTP 200 OK"
    color = color_success

    url = link.get_attribute('href')

    if not url:
        status = "ERROR. LINK WITH NO HREF"
        color = color_error
        broken_links += 1
    elif 'mailto' in url:
        status = "MAIL LINK (NEEDS MANUAL CHECK)"
        color = color_warning
    else:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 403 or response.status_code == 401:
                color = color_warning
                status = "AUTHORIZATION REQUIRED FOR LINK (NEEDS MANUAL CHECK)"
            elif response.status_code != 200:
                color = color_error
                status = "HTTP " + str(response.status_code)
                broken_links += 1
        except requests.exceptions.Timeout:
            color = color_error
            status = "HTTP 408 Request Timeout"
            broken_links += 1

    print(f"{color}{text} - {status}{style('reset')}")
        

def page():
    main = driver.find_element(By.TAG_NAME, 'main')
    links = main.find_elements(By.TAG_NAME, 'a')

    for link in links:
        check_status(link)


def subsubmenu(subnav, subsubnav):
    subsubnav_items = subsubnav.find_elements(By.XPATH, '../ul/li/a')
    
    # navigates through subsub menu (lol)
    for subsubnav_item in subsubnav_items:
        text = subsubnav_item.find_element(By.TAG_NAME, 'span').get_attribute('textContent').strip()
        print(f"{color_submenu}--- {text} ---{style('reset')}")

        subnav.click()
        pause()
        driver.get(subsubnav_item.get_attribute('href'))
        page()
        pause()
        driver.back()
        pause()


def submenu(subnav):
    subnav_items = subnav.find_elements(By.XPATH, '../ul/li/a')
    
    # navigates through sub menu
    for subnav_item in subnav_items:
        text = subnav_item.find_element(By.TAG_NAME, 'span').get_attribute('textContent').strip()
        print(f"{color_submenu}--- {text} ---{style('reset')}")

        li = subnav_item.find_element(By.XPATH, '..')

        subnav.click()
        pause()
        # subnav_item.click()
        driver.get(subnav_item.get_attribute('href'))
        page()
        pause()
        driver.back()
        pause()

        if 'has-submenu' in li.get_attribute('class'):    
            subsubmenu(subnav, subnav_item) 


def menu():
    nav = driver.find_elements(By.TAG_NAME, "nav")
    nav_main = nav[2]
    nav_items = nav_main.find_elements(By.XPATH, './div/div/ul/li/a')

    # navigates through menu
    for nav_item in nav_items:
        text = nav_item.find_element(By.TAG_NAME, 'span').text.upper()
        print(f"{color_menu}===== {text} ====={style('reset')}")

        if 'menu__link-sub' in nav_item.get_attribute('class'):
            submenu(nav_item)
        else:
            nav_item.click()
            page()
            driver.back()
        

def main():
    print(broken_links)
    print(f"{color_prompt}Starting broken link check automation...{style('reset')}")
    menu()
    print(f"{color_prompt}Done!{style('reset')}")

    color = color_success if broken_links == 0 else color_error

    print(f"There were {color}{str(broken_links)} broken links{style('reset')}.")

if __name__ == '__main__':
    main()
