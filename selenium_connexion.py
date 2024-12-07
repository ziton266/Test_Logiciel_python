
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Démarrer le navigateur
driver = webdriver.Chrome()

try:
    # Étape 1 : Accéder à la page d'accueil
    driver.get("https://www.saucedemo.com/")

    # Étape 2 : Se connecter avec des identifiants valides
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    # Étape 3 : Attendre que la page d'inventaire se charge
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )

    # Étape 4 : Vérifier que la connexion est réussie
    user_icon = driver.find_element(By.CLASS_NAME, "bm-burger-button")
    assert user_icon.is_displayed(), "L'icône utilisateur n'est pas affichée, la connexion a échoué."

    # Capture d'écran pour la réussite du test
    driver.save_screenshot("connexion_reussie.png")
    print("Connexion réussie, capture d'écran effectuée.")

except Exception as e:
    print(f"Erreur lors du test de connexion : {e}")

finally:
    # Fermer le navigateur
    driver.quit()
