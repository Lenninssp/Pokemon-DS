import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import pandas as pd

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
    all_pokemons = driver.find_elements(By.XPATH, ' //div[@data-component-type="s-search-result"]')
    
    for pokemon in all_pokemons:
        # name ## //span[@class='a-size-base-plus a-color-base a-text-normal']
        names = pokemon.find_elements(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']")
        for name in names:
            pokemon_names.append(name.text)
        # price
        prices = pokemon.find_elements(By.XPATH, ".//span[@class='a-price-whole']")
        for price in prices:
            pokemon_prices.append(price.text)
        #reviews
        try:
            if(pokemon.find_elements(By.XPATH, ".//span[@class='a-size-base s-underline-text']"))>0:
                reviews = pokemon.find_elements(By.XPATH, ".//span[@class='a-size-base s-underline-text']")
                for review in reviews:
                    pokemon_reviews.append(review.text)
            else:
                pokemon_reviews.append("0")
                
        except:
            pass 



    print(len(pokemon_names))
    print(len(pokemon_prices))
    print(len(pokemon_reviews))

    df = pd.DataFrame(zip(pokemon_names,pokemon_prices,pokemon_reviews), columns=['pokemon_names','pokemon_prices','pokemon_reviews'])
    df.to_csv("/Users/lenninsabogal/Coding/Python/jupyters/pokemon/amazon_scraper/pokemon_prices.csv",index=False)

iniciar("pokemon")



