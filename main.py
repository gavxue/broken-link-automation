from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
from colored import fore, back, style

# url of site to check
url = "https://uwaterloo.ca/civil-environmental-engineering-information-technology"
# url = "https://uwaterloo.ca/civil-environmental-engineering"
# url = "https://uwaterloo.ca/engineering/"


driver = webdriver.Chrome()
driver.get(url)

# counter
broken_links = 0

# colours
color_success = f"{fore('green')}"
color_error = f"{fore('red')}"
color_warning = f"{fore('yellow')}"
color_menu = f"{style('bold')}{fore('magenta')}{back('yellow')}"
color_submenu = f"{style('bold')}{fore('blue')}"
color_prompt = f"{fore('cyan')}"

# request headers
headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json'
}

# link object
class Link:
    def __init__(self, title, url):
        self.title = title
        self.url = url

# pause function
def pause():
    time.sleep(0.5)


# checks a single link
def check_status(link):
    global broken_links

    text = ' '.join(link.get_attribute('textContent').split())
    status = "HTTP 200 OK"
    color = color_success

    url = link.get_attribute('href')

    if not url:
        # no url
        status = "ERROR. LINK WITH NO URL"
        color = color_error
        broken_links += 1
    elif 'mailto' in url:
        # mail link
        status = "MAIL LINK (NEEDS MANUAL CHECK)"
        color = color_warning
    else:
        try:
            # send request
            response = requests.get(url, timeout=10, headers=headers)
            if response.status_code == 403 or response.status_code == 401:
                # authorization required
                color = color_warning
                status = "AUTHORIZATION REQUIRED FOR LINK (NEEDS MANUAL CHECK)"
            elif response.status_code != 200:
                # not successful
                color = color_error
                status = "HTTP " + str(response.status_code)
                broken_links += 1
        except requests.exceptions.Timeout:
            # request timed out
            color = color_error
            status = "HTTP 408 Request Timeout"
            broken_links += 1
        except:
            # unknown error
            color = color_error
            status = "Unknown error occured (needs manual check)"
            broken_links += 1

    print(f"{color}{text} - {status}{style('reset')}")
        

# checks a single page
def page():
    # get page main content
    main = driver.find_element(By.TAG_NAME, 'main')
    links = main.find_elements(By.TAG_NAME, 'a')

    # check all links on page
    for link in links:
        check_status(link)


# iterates through menu
def menu():
    nav = driver.find_elements(By.TAG_NAME, "nav")
   
    a = nav[2].find_elements(By.TAG_NAME, 'a')
    if len(nav) == 4:
        a = a + nav[3].find_elements(By.TAG_NAME, 'a')      # if there is a secondary nav
    
    # get all menu items
    nav_items = []
    for link in a:
        if link.get_attribute('href'):
            nav_items.append(Link(link.get_attribute('textContent').strip(), link.get_attribute('href')))

    # check each menu item
    for nav_item in nav_items:
        print(f"{color_menu}--- {nav_item.title} ---{style('reset')}")
        driver.get(nav_item.url)
        page()
        

def main():
    print(f"{color_prompt}Starting broken link check automation...{style('reset')}")
    menu()
    print(f"{color_prompt}Done!{style('reset')}")

    color = color_success if broken_links == 0 else color_error

    print(f"There were {color}{str(broken_links)} broken links{style('reset')}.")


if __name__ == '__main__':
    main()
