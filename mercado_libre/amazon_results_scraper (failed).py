from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
from selenium.webdriver.common.by import By
import requests
import json
import time

def search_amazon(item):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.amazon.com') 
    driver.implicitly_wait(5)
    search_box = driver.find_element (By.ID,'twotabsearchtextbox').send_keys(item)
    search_button = driver.find_element(By.ID,'nav-search-submit-button').click()
    driver.implicitly_wait(5)

    try:
        num_page = driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[67]/div/div/span/span[4]')
    except NoSuchElementException:
        num_page=driver.find_element(By.CLASS_NAME, 's-pagonation-item').click()

    driver.implicitly_wait(3)

    url_list=[]

    for i in range (int(num_page.text)):
        page_ = i + 1
        url_list.append(driver.current_url)
        driver.implicitly_wait(4)
        click_next = driver.find_element(By.CLASS_NAME,'s-pagonation-item').click()
        print("Page " + str(page_) + " grabbed")

    driver.quit()

    with open('search_results_urls.txt', 'w') as filehandle:
        for result_page in url_list:
            filehandle.write('%s\n' % result_page)
    print("---DONE---")

def scrape(url):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)

search_amazon('pokemon peluche') # <------ search query goes here.

e = Extractor.from_yaml_file('search_results.yml')

# product_data = []
with open("search_results_urls.txt",'r') as urllist, open('search_results_output.jsonl','w') as outfile:
    for url in urllist.read().splitlines():
        data = scrape(url)
        if data:
            for product in data['products']:
                product['search_url'] = url
                print("Saving Product: %s"%product['title'].encode('utf8'))
                json.dump(product,outfile)
                outfile.write("\n")
                # sleep(5)