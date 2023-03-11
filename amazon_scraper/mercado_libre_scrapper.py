import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# //span[text()='']

def iniciar (item):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.mercadolibre.com.co/")
    driver.maximize_window()

    entendido_button = driver.find_element(By.XPATH, "//button[@class='cookie-consent-banner-opt-out__action cookie-consent-banner-opt-out__action--primary cookie-consent-banner-opt-out__action--key-accept']")
    entendido_button.click()

    search_box = driver.find_element(By.CLASS_NAME, "nav-search-input")
    search_box.clear()
    search_box.send_keys(item)

    search_button = driver.find_element(By.CLASS_NAME, "nav-search-btn")
    search_button.click()

    next_button = driver.find_element(By.XPATH, ".//a[@class='andes-pagination__link shops__pagination-link ui-search-link']")

    #driver.find_element(By.XPATH, "//span[text()='Sólo en Existencias']").click()

    #driver.find_element(By.XPATH, "//span[text()='Elegible para Envío Gratis']").click()

    pokemon_names = []
    pokemon_prices = [[],[],[]]

    # all itlems
    for _ in range(3):
        all_pokemons = driver.find_elements(By.XPATH, "//div[@class='ui-search-result__wrapper shops__result-wrapper']")
        next_button = driver.find_element(By.XPATH, ".//a[@title='Siguiente']")
        
        for pokemon in all_pokemons:
            # name ## //span[@class='a-size-base-plus a-color-base a-text-normal']
            names = pokemon.find_elements(By.XPATH, ".//h2[@class='ui-search-item__title shops__item-title']")
            for name in names:
                pokemon_names.append(name.text)
            # price
            prices = pokemon.find_elements(By.XPATH, ".//span[@class='price-tag-fraction']")
            for m , price in enumerate(prices):
                try:
                    pokemon_prices[m].append(price.text)
                except NoSuchElementException:
                    pokemon_prices[m].append("0")
                
        next_button.click()
                
    #print(pokemon_names,pokemon_prices[0], pokemon_prices[1],pokemon_prices[2])

    df = pd.DataFrame(zip(pokemon_names,pokemon_prices[0], pokemon_prices[1],pokemon_prices[2]), columns=['pokemon_names','pokemon_prices 1','pokemon_prices 2','pokemon_prices 3'])

    df = df.reset_index()
    df = df.rename (columns={'index':'contador'})
    
    print(df)
    df.to_csv("/Users/lenninsabogal/Coding/Python/jupyters/pokemon/amazon_scraper/pokemon_prices.csv",index=False)
    df.to_excel("/Users/lenninsabogal/Coding/Python/jupyters/pokemon/amazon_scraper/pokemon_prices.xlsx",index=False)

iniciar("peluches pokemon")




