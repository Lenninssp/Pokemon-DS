import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def iniciar (item):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    driver.get("https://www.mercadolibre.com.co/")
    #driver.maximize_window()

    entendido_button = driver.find_element(By.XPATH, "//button[@class='cookie-consent-banner-opt-out__action cookie-consent-banner-opt-out__action--primary cookie-consent-banner-opt-out__action--key-accept']")
    entendido_button.click()

    search_box = driver.find_element(By.CLASS_NAME, "nav-search-input")
    search_box.clear()
    search_box.send_keys(item)

    search_button = driver.find_element(By.CLASS_NAME, "nav-search-btn")
    search_button.click()

    next_button = driver.find_element(By.XPATH, ".//a[@class='andes-pagination__link shops__pagination-link ui-search-link']")

    pokemon_columns = [[],[],[],[],[],[],[],[]]
    pokemon_columns_list = ["Marca", "Línea", "Modelo", "Es kit", "Forma del peluche", "Personaje", "Tamaño"]

    contador=0
    # all itlems
    for _ in range(39): 
        
        all_pokemons = driver.find_elements(By.XPATH, "//div[@class='ui-search-result__wrapper shops__result-wrapper']")

        for a,pokemon in enumerate(all_pokemons):
            print(f"pokemon {contador} ---------")
            contador+=1

            all_pokemons = driver.find_elements(By.XPATH, "//div[@class='ui-search-result__wrapper shops__result-wrapper']")
            pokemon = all_pokemons[a]
            num=pokemon.find_element(By.XPATH, ".//a[@class='ui-search-item__group__element shops__items-group-details ui-search-link']")
            num.click()

            elementos1 = driver.find_elements(By.XPATH, "//th[@class='andes-table__header andes-table__header--left ui-pdp-specs__table__column ui-pdp-specs__table__column-title']")
            elementos2 = driver.find_elements(By.XPATH, "//span[@class='andes-table__column--value']")

            #print(elementos1[0].text, elementos2[0].text)

            i = 0
            while i < len(pokemon_columns_list):
                if i < len(elementos1) and elementos1[i].text == pokemon_columns_list[i]:
                    pokemon_columns[i].append(elementos2[i].text)
                else:
                    pokemon_columns[i].append("/")
                i += 1

            price_box = driver.find_element(By.XPATH, "//span[@class='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact']")
            price = price_box.find_element(By.XPATH, ".//span[@class='andes-money-amount__fraction']")
            
            pokemon_columns[7].append(price.text)

            #print(pokemon_columns[6])

            driver.execute_script("window.history.go(-1)")
            
        next_button = driver.find_element(By.XPATH, ".//a[@title='Siguiente']")
        next_button.click()



    #print(pokemon_names,pokemon_prices[0], pokemon_prices[1],pokemon_prices[2])
    #for a,b in enumerate(pokemon_names):
    #    print(a,b)

    df = pd.DataFrame({k: v for k, v in zip(pokemon_columns_list, pokemon_columns)})

    df = df.reset_index()
    df = df.rename (columns={'index':'contador'})
    
    print(df)
    df.to_csv("/Users/lenninsabogal/Coding/Python/jupyters/pokemon/mercado_libre/pokemon_prices2.csv",index=False)
    df.to_excel("/Users/lenninsabogal/Coding/Python/jupyters/pokemon/mercado_libre/pokemon_prices2.xlsx",index=False) 

iniciar("pokemon peluche")




