from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException

def test_filtering():
    driver = webdriver.Chrome()

    try:
        # Open the website
        driver.get("https://www.saucedemo.com/")

        # Wait for and input username and password
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        password = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_button.click()

        # Wait for the inventory list to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Select the filter dropdown
        filter_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))

        # Define filter tests (only name-related filters)
        filtering_tests = [
            ("Name (A to Z)", "az", lambda x, y: x <= y),
            ("Name (Z to A)", "za", lambda x, y: x >= y)
        ]

        # Test each filter
        for filter_name, filter_value, comparison_func in filtering_tests:
            filter_dropdown.select_by_value(filter_value)

            # Wait for the inventory list to update
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
            )

            # Get item names
            names = get_item_names(driver)

            # Check sorting order
            is_ordered = all(comparison_func(names[i], names[i + 1]) for i in range(len(names) - 1))

            assert is_ordered, f"Filter '{filter_name}' did not sort correctly."
            print(f"Filter '{filter_name}' passed.")

        driver.save_screenshot("filtrage_reussi.png")
        print("Filtering tests completed successfully.")

    except Exception as e:
        print(f"Error during filtering tests: {e}")
        driver.save_screenshot("erreur_filtrage.png")

    finally:
        driver.quit()


def get_item_names(driver):
    try:
        # Wait for inventory items to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")

        names = [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in items]

        return names
    except StaleElementReferenceException:
        # Retry in case of stale element reference
        return get_item_names(driver)


if __name__ == "__main__":
    test_filtering()
