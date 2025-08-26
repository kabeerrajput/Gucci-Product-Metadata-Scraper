import os
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumUtils:
    def __init__(self, proxies_list):
        self.driver = self.initialize_chrome_webdriver(proxies_list)

    def initialize_chrome_webdriver(self, proxies_list):
        print('initialize_chrome_webdriver start.')
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-session-crashed-bubble")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f'--proxy-server=http://{proxy}')
        chrome_driver = webdriver.Chrome(options=chrome_options)
        return chrome_driver

    def go_to_url(self, url):
        try:
            print("navigating_to_URL start")
            self.driver.get(url)
            print("navigating_to_URL end")
        except Exception as e:
            print("URL not found error: ", url)

    def wait_for_element_presence(self, xpath, wait_secs=60, By=By.XPATH):
        try:
            print("wait_for_element_presence start")
            WebDriverWait(self.driver, wait_secs).until(EC.presence_of_element_located((By, xpath)))
            print("wait_for_element_presence end")
        except Exception as e:
            print(f"wait_for_element_presence Failed {e} XPath :: {xpath}")

    def wait_for_loading_to_finish(self, xpath, wait_secs=60, By=By.XPATH):
        try:
            print("wait_for_loading_to_finish start")
            element = WebDriverWait(self.driver, wait_secs).until(EC.invisibility_of_element_located((By, xpath)))
            print(f"wait_for_loading_to_finish end")
        except Exception as e:
            print(f"wait_for_loading_to_finish Failed {e} XPath :: {xpath}")

    def wait_for_element_intractable(self, xpath, wait_secs="", By=By.XPATH):
        if wait_secs == "":
            wait_secs = 60
        try:
            print("wait_for_element_intractable start")
            element = WebDriverWait(self.driver, wait_secs).until(EC.visibility_of_element_located((By, xpath)))
            print(f"wait_for_element_intractable end")
        except Exception as e:
            # print(f"wait_for_element_intractable Failed {e} XPath :: {xpath}")
            print(f"wait_for_element_intractable Failed XPath :: {xpath}")

    def click_element(self, xpath, By=By.XPATH):
        try:
            element = self.get_element(xpath)
            if element is not False:
                element.click()
        except Exception as e:
            print(f"Click Failed:: Error {e} XPath :: {xpath}")

    def switch_to_iframe(self, iframe_path="", wait_secs="", By=By.XPATH):
        try:
            print("switch_to_iframe start")
            if wait_secs == "":
                wait_secs = 60
            if iframe_path == "":
                self.driver.switch_to.parent_frame()
            else:
                element = WebDriverWait(self.driver, wait_secs).until(
                    EC.frame_to_be_available_and_switch_to_it((By, iframe_path)))
            # else:
            #     iframe_element = self.driver.find_element(iframe_path)
            #     if iframe_element is not False:
            #         self.driver.switch_to.frame(iframe_element)
            print("switch_to_iframe end")
        except Exception as e:
            # print(f"switch_to_iframe Failed:: Error {e} XPath:: {iframe_path}")
            print(f"switch_to_iframe Failed:: Error XPath:: {iframe_path}")

    def get_element(self, xpath, By=By.XPATH):
        try:
            element = self.driver.find_element(By, xpath)
            if element not in [False, None]:
                return element
        except Exception as e:
            print(f"get_element Failed:: Error {e} XPath:: {xpath}")
            return False

    def get_elements(self, xpath, By=By.XPATH):
        try:
            elements = self.driver.find_elements(By, xpath)
            if len(elements) > 0 and elements not in [None, False]:
                return elements
        except Exception as e:
            print(f"get_elements Failed:: Error {e} XPath:: {xpath}")

    def get_element_text(self, xpath, By=By.XPATH):
        try:
            element_text = self.get_element(xpath).text
            if element_text not in ["", None, False]:
                return element_text
        except Exception as e:
            print(f"get_element_text Failed:: Error {e} XPath:: {xpath}")

    def fill_keys_value(self, xpath, keys_value, By=By.XPATH):
        try:
            element = self.get_element(xpath)
            element.send_keys(keys_value)
            time.sleep(0.5)
        except Exception as e:
            print(f"fill_keys_value Failed:: Error {e} XPath:: {xpath}")

    def scroll_to_element(self, xpath, By=By.XPATH):
        try:
            element = self.get_element(xpath)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(0.1)
        except Exception as e:
            print(f"scroll_to_element Failed:: Error {e} XPath:: {xpath}")

    def hover_over_element(self, xpath, By=By.XPATH):
        try:
            element = self.get_element(xpath, By)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            time.sleep(0.2)
            print("hovered on a element")
        except Exception as e:
            print(f"hover_over_element Failed:: Error {e} XPath:: {xpath}")

    def wait_for_element_clickable(self, xpath, wait_secs=60, By=By.XPATH):
        try:
            print("wait_for_element_clickable start")
            WebDriverWait(self.driver, wait_secs).until(EC.element_to_be_clickable((By, xpath)))
            print("wait_for_element_clickable end")
        except Exception as e:
            print(f"wait_for_element_clickable Failed {e} XPath :: {xpath}")

    def wait_for_element_to_invisible(self, element, wait_secs=60, By=By.XPATH):
        try:
            print("wait_for_element_to_invisible start")
            element = WebDriverWait(self.driver, wait_secs).until(EC.invisibility_of_element(element))
            print(f"wait_for_element_to_invisible end")
        except Exception as e:
            print(f"wait_for_element_to_invisible Failed {e} Element :: {str(element)}")

    def isElementPresent(self, xpath, By=By.XPATH):
        try:
            element = self.driver.find_element(By, xpath)
            if element not in [False, None]:
                return True
            else:
                return False
        except NoSuchElementException:
            return False
        except Exception as e:
            print(f"isElementPresent Failed:: Error {e} XPath:: {xpath}")
            return False

    def take_screenshot(self, dir, file_name=""):
        try:
            self.driver.save_screenshot(file_name)
        except Exception as error:
            print(f"take_screenshot() Error: {error}")

    def close_session(self):
        self.driver.quit()

    def fill_keys_value_by_script(self, value, value_element):
        try:
            element = self.get_element(value_element)
            self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
        except Exception as error:
            print(f"fill_keys_value_by_script() Error: {error}")

    import os

    def take_screenshot_with_directory(self, dir, file_name="screenshot.png"):
        try:
            # Ensure the directory exists
            os.makedirs(dir, exist_ok=True)

            # Force .png extension
            if not file_name.lower().endswith(".png"):
                file_name += ".png"

            full_path = os.path.join(dir, file_name)

            # Save screenshot
            self.driver.save_screenshot(full_path)
            print(f"Screenshot saved at: {full_path}")
        except Exception as error:
            print(f"take_screenshot() Error: {error}")
