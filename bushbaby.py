""" Code that uses selenium-stealth to generate a sneaky headless browser for scraping activities on sites which attempt
to block scrapers. """

import os
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


class BushBaby:
    """"Named after the furtive creature of the African Night to reflect the cunningness of this code"""
    selenium_retries = 0

    def __init__(self, url):

        """Initiate the Request object with a url as a minimum. Other parameters can be passed into the Constructor """

        self.url = url

    def go_hunt_bushbaby(self):
        """ The main engine of the class which defines the characteristics of the selenium object and how it retrieves
        content"""
        try:
            # The block below this seeds the randomness for the user-agent details to disguise the automation framework
            software_names = [SoftwareName.CHROME.value, SoftwareName.EDGE.value, SoftwareName.ANDROID.value,
                              SoftwareName.FIREFOX.value]
            operating_systems = [OperatingSystem.WINDOWS.value,
                                 OperatingSystem.LINUX.value,
                                 OperatingSystem.MAC_OS_X.value,
                                 OperatingSystem.CHROMEOS.value]
            user_agent_rotator = UserAgent(software_names=software_names,
                                           operating_systems=operating_systems)
            user_agent = user_agent_rotator.get_random_user_agent()

            chrome_options = Options()
            # This is the path to the applicable chromedriver
            ser = f"{os.getcwd()}/chromedriver"

            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1420,1080")
            chrome_options.add_argument("-disable-gpu")
            chrome_options.add_argument(f"user-agent={user_agent}")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            self.web_browser = webdriver.Chrome(executable_path=ser, options=chrome_options)
            # Wrap it all up with Stealth
            stealth(self.web_browser,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
            self.web_browser.get(self.url)

        except WebDriverException:
            """This exception could probably be a bit more sophisticated."""
            print("There was a problem")


    def save_page_source(self, name_of_file):
        """Take the browser object and return the page content by saving it to a file to be parsed later. Note:
        /html/body and 'innerHTML' are generic DOM items and should always work. Additional methods for parsing
        elements could be written into this as needed. eg. web_browser.find_element(By.TAG_NAME, value='img' and so
        on. """

        page_source = self.web_browser.find_element(By.XPATH, value="/html/body")

        with open(f"{name_of_file}.txt", "w") as input_file:
            input_file.writelines(page_source.get_attribute('innerHTML'))
