import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 

# //span[text()='']

def iniciar (item):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.amazon.com")

    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.clear()
    search_box.send_keys(item)

    search_button = driver.find_element(By.ID, "nav-search-submit-button")
    search_button.click()

    #driver.find_element(By.XPATH, "//span[text()='Elegible para Envío Gratis']").click()

    pokemon_names = []
    pokemon_prices = []
    pokemon_reviews = []

    # all itlems
    # name ## //span[@class='a-size-base-plus a-color-base a-text-normal']
    names = driver.find_elements(By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")
    for name in names:
        pokemon_names.append(name.text)
    # price
    prices = driver.find_elements(By.XPATH, "//span[@class='a-price-whole']")
    for price in prices:
        pokemon_prices.append(price.text)
    #reviews
    reviews = driver.find_elements(By.XPATH, "//span[@class='a-size-base s-underline-text']")
    for review in reviews:
        pokemon_reviews.append(review.text)


    print(len(pokemon_names))
    print(len(pokemon_prices))
    print(len(pokemon_reviews))


iniciar("pokemon")



