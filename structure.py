#Selenium imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import time
import random

class RedditStructure:

    username = (By.CSS_SELECTOR, "input[name='username']")
    password = (By.CSS_SELECTOR, "input[name='password']") 
    submit = (By.XPATH, "//*[contains(text(), 'Log In')]")
    # save_information = (By.XPATH, "//div[contains(text(), 'Agora não') or contains(text(), 'Not now')]") 
    # not_now_notification = (By.XPATH, "//button[contains(text(), 'Agora não') or contains(text(), 'Not now')]") 
    
    # JScript to scroll a scroll bar
    js_script_to_scroll = """ 
        arguments[0].scrollTo(0, arguments[0].scrollHeight);
        return arguments[0].scrollHeight; """
    
    # --------------------------------------------------------------------
    
    @staticmethod
    def __get_random_sleep__(minimum, maximum):        
        time.sleep(random.uniform(minimum, maximum))
    
    
    @staticmethod
    def sleep(time):      
        RedditStructure.__get_random_sleep__(time-2, time+2) if time >= 2 else RedditStructure.__get_random_sleep__(0, 5)

    @staticmethod
    def get_json_name_from_url(url):
        print(url)
        _, _, _, _, subreddit, _, ident, _, _ = url.split('/') # FIXME: 4 to unpack instead of 9
        query = query.split('&')[0]
        return f"{subreddit}-{ident}"


    @staticmethod
    def get_login_clickable(driver, find=True):
        xpath = "//span[contains(text(), 'Log In')]"
        return driver.find_element(By.XPATH, xpath) if find else (By.XPATH, xpath)
    
    
    @staticmethod
    def get_search_input(driver, find=True):
        css_selector = "input[placeholder='search']"
        return driver.find_element(By.CSS_SELECTOR, css_selector) if find else (By.CSS_SELECTOR, css_selector)
        

    @staticmethod
    def get_all_posts_clickable(driver, find=True):
        xpath = "//*[@class='search-result-header']"
        return driver.find_elements(By.XPATH, xpath) if find else (By.XPATH, xpath)
            

    # @staticmethod
    # def get_post_url_from_post_str(post, find=True):
    #     xpath = ".//a[1]"
    #     return str(post.find_element(By.XPATH, xpath).href) if find else (By.XPATH, xpath)


    @staticmethod
    def get_post_title(driver, find=True):
        xpath = "//*[@class='title']" # FIXME
        return driver.find_element(By.XPATH, xpath) if find else (By.XPATH, xpath)
    

    @staticmethod
    def get_post_itself(driver, find=True):
        xpath = "//*[@class='entry unvoted']/*[@class='md']"
        try:
            return driver.find_element(By.XPATH, xpath) if find else (By.XPATH, xpath)
        except:
            return None
        

    @staticmethod
    def get_all_expand_comments_clickable(driver, find=True):
        xpath1 = "//*[@class='expand']"
        xpath2 = "//*[@class='morecomments']"
        return list(driver.find_elements(By.XPATH, xpath1)).extend(list(driver.find_elements(By.XPATH, xpath2))) if find else (By.XPATH, [xpath1, xpath2])


    @staticmethod
    def get_parent_from_comment(comment, find=True):
        xpath = "//*[@class='parent']//a[1]"
        return comment.find_element(By.XPATH, xpath) if find else (By.XPATH, xpath)


    @staticmethod
    def get_comment_itself_from_comment(comment, find=True):
        xpath = "//*[@class='md']"
        return comment.find_element(By.XPATH, xpath) if find else (By.XPATH, xpath)


    # @staticmethod
    # def get_post_time(driver, find=True):  
    #     xpath = "//*[@class='entry unvoted']/*time[]"     
    #     return driver.find_element(By.XPATH, xpath).get_attribute('datetime') if find else (By.XPATH, xpath)


    # @staticmethod
    # def get_sort_by_clickable(driver, find=True):
    #     xpath = "//div[@class='search-menu']/*[last()]"
        