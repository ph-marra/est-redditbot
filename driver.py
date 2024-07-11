#Selenium imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from structure import RedditStructure

class RedditDriver:
    
    def __init__(self, username, password):        
        self.username = username
        self.password = password
        self.driver_directory = None
        self.driver = None
        self.mounted = False
        self.logged_in = False
        
        
    def mount_driver(self, driver_directory=None, overwrite=False):        
        # If directory not passed or there is already an opened driver and overwrite=False
        if driver_directory is None or (overwrite is False and self.driver is not None):
            raise Exception("Error found while mounting driver")
        
        # If should overwrite and there is an opened driver, quit it before opening new driver
        if overwrite is True and self.driver is not None:
            self.quit()
        
        self.driver_directory = driver_directory
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-fullscreen")

        self.driver = webdriver.Chrome(options=self.options)
        self.mounted = True
        
        
    def login(self, timeout=5):       
        if self.driver is None:
            raise Exception("Driver not mounted")
            
        if timeout < 0:
            raise Exception("Invalid timeout")
        
        self.driver.get("https://old.reddit.com/login")

        # WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(RedditStructure.get_login_clickable(self.driver, find=False))).click()
        
        username = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(RedditStructure.username))
        password = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(RedditStructure.password))
        username.clear()
        password.clear()
        username.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)
        
        # WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(RedditStructure.submit)).click()
        RedditStructure.sleep(10)

        self.logged_in = True
        

    def quit(self):        
        self.driver.quit()
        self.driver = None
        self.mounted = False
        self.logged_in = False
        
        