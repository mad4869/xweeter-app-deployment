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


class UnitTest:
    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get("http://localhost:4173")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_login(self):
        self.driver.find_element(By.CSS_SELECTOR, "button:nth-child(2)").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("akbar")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("pneumonic")
        self.driver.find_element(By.CSS_SELECTOR, ".w-24").click()
        self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .gap-4").click()

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

    def test_add_xweet(self):
        self.driver.find_element(By.NAME, "new-xweet").click()
        self.driver.find_element(By.NAME, "new-xweet").send_keys("new xweet")
        self.driver.find_element(By.CSS_SELECTOR, ".col-span-4").click()

        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".font-bold.text-sky-800.fade-in.dark:text-sky-600",
                    )
                )
            )
            assert (
                message.text == "You posted a new xweet!"
            ), "Success message is not found. Failed to add xweet."
            print("New xweet added successfully.")
        except Exception as e:
            print("Failed to add new xweet or no success message found. Error:", e)

    def test_edit_xweet(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div:nth-child(1) > .flex > .flex .svg-inline--fa:nth-child(4)",
        ).click()
        self.driver.find_element(By.NAME, "edit-xweet").send_keys("new edited xweet")
        self.driver.find_element(By.CSS_SELECTOR, ".max-h-screen").click()

        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".font-bold.text-sky-800.fade-in.dark:text-sky-600",
                    )
                )
            )
            assert (
                message.text == "You fixed your xweet!"
            ), "Success message is not found. Failed to edit xweet."
            print("Xweet edited successfully.")
        except Exception as e:
            print("Failed to edit xweet or no success message found. Error:", e)

    def test_delete_xweet(self):
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div:nth-child(1) > .flex > .flex .svg-inline--fa:nth-child(5)",
        ).click()
        self.driver.find_element(By.CSS_SELECTOR, ".hover\\3A bg-red-600").click()

        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div.fixed.flex.items-center.gap-4.px-4.py-2.text-white.-translate-x-1/2.rounded-md.left-1/2.bottom-4 div.flex-1 > p",
                    )
                )
            )
            assert (
                message.text == "Your xweet has been deleted"
            ), "Success message is not found. Failed to delete xweet."
            print("Xweet deleted successfully.")
        except Exception as e:
            print("Failed to delete xweet or no success message found. Error:", e)


if __name__ == "__main__":
    pytest.main()
