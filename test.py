import unittest, os
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class AllTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the browser (headless option can be used if desired)
        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')  # Uncomment to run in headless mode
        cls.browser = webdriver.Firefox(options=option)

        # Set the base URL
        try:
            cls.url = os.environ['URL']
        except KeyError:
            cls.url = "http://localhost/uas"

    def login(self):
        self.browser.get(f"{self.url}/login.php")
        self.browser.find_element(By.ID, "inputUsername").send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

    def wait_for_url(self, url, timeout=10):
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.current_url == url
        )

    # Login Test Case
    def test_1_valid_login(self):
        self.browser.get(f"{self.url}/login.php")
        expected_result = "Howdy, damn admin!"
        self.browser.find_element(By.ID, "inputUsername").send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        actual_result = self.browser.find_element(By.XPATH, "//div[@class='container']/h2").text
        self.assertIn(expected_result, actual_result)

    def test_2_invalid_login(self):
        self.browser.get(f"{self.url}/logout.php")
        expected_result = "Damn, wrong credentials!!"
        self.browser.find_element(By.ID, "inputUsername").send_keys("admin")
        self.browser.find_element(By.ID, "inputPassword").send_keys("admin")
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        actual_result = self.browser.find_element(By.XPATH, "//div[@class='checkbox mb-3']/label").text
        self.assertIn(expected_result, actual_result)

    # Contact Management Test Cases
    def test_3_add_new_contact(self):
        self.login()
        self.browser.get(f"{self.url}/create.php")
        self.browser.find_element(By.ID, 'name').send_keys("Sir Yon")
        self.browser.find_element(By.ID, 'email').send_keys("sir.yon@ex.com")
        self.browser.find_element(By.ID, 'phone').send_keys("123456789")
        self.browser.find_element(By.ID, 'title').send_keys("Tester")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_4_delete_contact(self):
        self.login()
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][5]//td[contains(@class, 'actions')]")
        delete_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-danger')]")
        delete_button.click()
        self.browser.switch_to.alert.accept()
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    def test_5_update_contact(self):
        self.login()
        actions_section = self.browser.find_element(By.XPATH, "//tr[@role='row'][3]//td[contains(@class, 'actions')]")
        update_button = actions_section.find_element(By.XPATH, ".//a[contains(@class, 'btn-success')]")
        update_button.click()
        self.browser.find_element(By.ID, 'name').clear()
        self.browser.find_element(By.ID, 'name').send_keys("Taruna Sakti")
        self.browser.find_element(By.ID, 'email').clear()
        self.browser.find_element(By.ID, 'email').send_keys("taruna.perisai@example.com")
        self.browser.find_element(By.ID, 'phone').clear()
        self.browser.find_element(By.ID, 'phone').send_keys("987654321")
        self.browser.find_element(By.ID, 'title').clear()
        self.browser.find_element(By.ID, 'title').send_keys("Knight")
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.assertEqual(self.browser.current_url, f"{self.url}/index.php")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2, warnings='ignore')
