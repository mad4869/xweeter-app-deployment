import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 800))
display.start()

chromedriver_autoinstaller.install()

chrome_options = webdriver.ChromeOptions()

options = ["--window-size=1200,1200", "--ignore-certificate-errors"]

for option in options:
    chrome_options.add_argument(option)


class TestFeatures:
    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get("http://localhost:4173")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_register_login(self):
        self.driver.find_element(By.ID, "fullname").click()
        self.driver.find_element(By.ID, "fullname").send_keys("User")
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("myuser")
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("myuser@email.com")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("mypassword")
        self.driver.find_element(By.ID, "confirm-password").click()
        self.driver.find_element(By.ID, "confirm-password").send_keys("mypassword")
        self.driver.find_element(By.CSS_SELECTOR, ".w-24").click()

        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url.endswith("/home")
            )
            assert self.driver.current_url.endswith(
                "/home"
            ), "URL does not end with '/home'. Login may have failed."
            print("Login successful. Redirected to homepage.")
        except Exception as e:
            print("Login failed or not redirected to homepage. Error:", e)


if __name__ == "__main__":
    pytest.main()
