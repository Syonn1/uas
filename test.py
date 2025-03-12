import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AllTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the browser
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')  # Uncomment to run in headless mode
        cls.browser = webdriver.Firefox(options=option)

        # Set the base URL
        cls.url = os.getenv("URL", "http://localhost/uas")

    def login(self):
        """Login function with WebDriverWait for elements"""
        self.browser.get(f"{self.url}/login.php")
        wait = WebDriverWait(self.browser, 10)

        try:
            wait.until(EC.presence_of_element_located((By.ID, "inputUsername"))).send_keys("admin")
            wait.until(EC.presence_of_element_located((By.ID, "inputPassword"))).send_keys("nimda666!")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        except NoSuchElementException as e:
            self.fail(f"Login failed, element not found: {e}")

    def wait_for_url(self, url, timeout=10):
        """Wait until the URL changes to the expected one"""
        WebDriverWait(self.browser, timeout).until(lambda driver: driver.current_url == url)

    def test_1_valid_login(self):
        """Test valid login with WebDriverWait"""
        self.browser.get(f"{self.url}/login.php")
        expected_result = "Howdy, damn admin!"
        wait = WebDriverWait(self.browser, 10)

        try:
            wait.until(EC.presence_of_element_located((By.ID, "inputUsername"))).send_keys("admin")
            wait.until(EC.presence_of_element_located((By.ID, "inputPassword"))).send_keys("nimda666!")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
            actual_result = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='container']/h2"))).text
            self.assertIn(expected_result, actual_result)
        except NoSuchElementException as e:
            self.fail(f"Test failed, element not found: {e}")

    def test_2_invalid_login(self):
        """Test invalid login with error message check"""
        self.browser.get(f"{self.url}/logout.php")
        expected_result = "Damn, wrong credentials!!"
        wait = WebDriverWait(self.browser, 10)

        try:
            wait.until(EC.presence_of_element_located((By.ID, "inputUsername"))).send_keys("admin")
            wait.until(EC.presence_of_element_located((By.ID, "inputPassword"))).send_keys("admin")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
            actual_result = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='checkbox mb-3']/label"))).text
            self.assertIn(expected_result, actual_result)
        except NoSuchElementException as e:
            self.fail(f"Test failed, element not found: {e}")

    def test_3_add_new_contact(self):
        """Test adding a new contact"""
        self.login()
        self.browser.get(f"{self.url}/create.php")
        wait = WebDriverWait(self.browser, 10)

        try:
            wait.until(EC.presence_of_element_located((By.ID, 'name'))).send_keys("Sir Yon")
            wait.until(EC.presence_of_element_located((By.ID, 'email'))).send_keys("sir.yon@ex.com")
            wait.until(EC.presence_of_element_located((By.ID, 'phone'))).send_keys("123456789")
            wait.until(EC.presence_of_element_located((By.ID, 'title'))).send_keys("Tester")
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]'))).click()
            self.assertEqual(self.browser.current_url, f"{self.url}/index.php")
        except NoSuchElementException as e:
            self.fail(f"Test failed, element not found: {e}")

    def test_4_delete_contact(self):
        """Test deleting a contact"""
        self.login()
        wait = WebDriverWait(self.browser, 10)

        try:
            actions_section = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[@role='row'][5]//td[contains(@class, 'actions')]")))
            delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
            delete_button.click()
            self.browser.switch_to.alert.accept()
            self.assertEqual(self.browser.current_url, f"{self.url}/index.php")
        except NoSuchElementException as e:
            self.fail(f"Test failed, element not found: {e}")

    def test_5_update_contact(self):
        """Test updating a contact"""
        self.login()
        wait = WebDriverWait(self.browser, 10)

        try:
            actions_section = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[@role='row'][3]//td[contains(@class, 'actions')]")))
            update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
            update_button.click()

            name_field = wait.until(EC.presence_of_element_located((By.ID, 'name')))
            name_field.clear()
            name_field.send_keys("Taruna Sakti")

            email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
            email_field.clear()
            email_field.send_keys("taruna.perisai@example.com")

            phone_field = wait.until(EC.presence_of_element_located((By.ID, 'phone')))
            phone_field.clear()
            phone_field.send_keys("987654321")

            title_field = wait.until(EC.presence_of_element_located((By.ID, 'title')))
            title_field.clear()
            title_field.send_keys("Knight")

            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]')))
            submit_button.click()
            
            self.assertEqual(self.browser.current_url, f"{self.url}/index.php")
        except NoSuchElementException as e:
            self.fail(f"Test failed, element not found: {e}")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
