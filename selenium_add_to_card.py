from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Démarrer le navigateur
driver = webdriver.Chrome()

try:
    # Étape 1 : Accéder à la page d'accueil
    driver.get("https://www.saucedemo.com/")

    # Étape 2 : Se connecter
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    # Étape 3 : Attendre que la liste des produits apparaisse
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    # Étape 4 : Ajouter un produit au panier
    add_to_cart_button = driver.find_element(By.XPATH, "//button[@data-test='add-to-cart-sauce-labs-backpack']")
    add_to_cart_button.click()

    # Étape 5 : Vérifier si le produit a été ajouté au panier
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_count.text == "1", "Le produit n'a pas été ajouté au panier correctement."

    # Capture d'écran après l'ajout au panier
    driver.save_screenshot("add_to_cart_success.png")
    print("Produit ajouté au panier avec succès, capture d'écran effectuée.")

except Exception as e:
    print(f"Erreur lors du test : {e}")

finally:
    # Fermer le navigateur
    driver.quit()
