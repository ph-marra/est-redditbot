#Selenium imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#Other imports here
import os
import wget
import time
import json
import copy
import random
import datetime
import os
import itertools

from structure import RedditStructure
from data import Post

class RedditBot:
    
    def __init__(self, reddit_driver):
        
        self.reddit_driver = reddit_driver
        self.driver = self.reddit_driver.driver
        
    
    def __get_list__(self, user=None, which='followers', sleep=5):   
        if which != 'followers' and which != 'following':
            raise Exception(f"Invalid list = {which}: choose either 'followers' or 'following'")
        
        # get the clickable scroll bar element and click it to open the followers/following page
        InstaStructure.get_followers_following_clickable(self.driver, which=which).click()
        InstaStructure.sleep(sleep)
        
        scroll_bar = InstaStructure.get_scroll_bar(self.driver, which)
        # height variable
        last_ht, ht = 0, 1
        
        # scroll the scroll bar until it reaches the bottom
        while last_ht != ht:
            last_ht = ht
            InstaStructure.sleep(sleep)
            ht = self.driver.execute_script(InstaStructure.js_script_to_scroll, scroll_bar)
    
        # once at the bottom, scrapes all links and names of followers/following
        links = InstaStructure.get_links(scroll_bar)
        names = [name.text for name in links if name.text != '']
        
        # return to the users page
        self.driver.back()
        
        return names
    
               
    def __get_posts__(self, user=None, pause=5):       
        # get driver internet page last height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        user.posts = {}
        last_post_fetched = None
        
        while True:
            
            # filter list (takes out all posts already fetched)
            if last_post_fetched is None:
                # get all visible posts (given driver)            
                visible_posts = InstaStructure.get_visible_posts(self.driver)
            else:
                last_post_fetched = visible_posts[-1]
                
                visible_posts = InstaStructure.get_visible_posts(self.driver)
                
                # remove first until first is not the last post fetched
                while visible_posts[0] != last_post_fetched:
                    visible_posts = visible_posts[1:]
                    
                # only last post fetched remains in the list so remove it
                visible_posts = visible_posts[1:]
                
            
            for post in visible_posts:
                
                # get post href (/p/href)
                post_href = InstaStructure.get_post_href(post)
                
                # creates a post object with only the current post href
                current_post = Post(post_href)
                
                # if post not already fetched, fetch it
                if post_href not in user.posts:
                
                    # open the post (post here is an page element)
                    post.click()
                    
                    # inserts attributes for the current post
                    self.__get_post_info__(current_post)
                    
                    # get back to user post grid
                    self.driver.back()

                    # adds the post to the users post dict
                    user.posts.update({post_href: current_post})
            
            # scroll the page to make more posts visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            InstaStructure.sleep(pause)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # will scroll the page until it can (until a new height is found)
            if new_height == last_height:
                break
                
            last_height = new_height
 

    def __get_post_info__(self, post=None, sleep=5):       
        if post is None or not isinstance(post, Post):
            raise Exception("Invalid post")
            
        InstaStructure.sleep(sleep)
        
        post.caption = InstaStructure.get_caption(self.driver)
        post.datetime = InstaStructure.get_datetime(self.driver)
    
    
    def get_users_info(self, user=None, sleep=5, get_followers=True, get_following=True, get_posts=True):       
        if user is None or not isinstance(user, User):
            raise Exception("Invalid user")
        
        self.driver.get(user.url)
        InstaStructure.sleep(sleep)
        
        if not InstaStructure.is_valid_handle(self.driver, user):
            raise Exception("Invalid user: handle invalid")
            
        if not InstaStructure.is_public(self.driver, user):
            raise Exception("Invalid user: private user")
                
        user.n_posts = int(InstaStructure.get_n_posts(self.driver).replace('.',''))
        user.followers = int(InstaStructure.get_followers(self.driver).replace('.',''))
        user.following = int(InstaStructure.get_following(self.driver).replace('.',''))
        user.name = InstaStructure.get_name(self.driver)
        user.bio = InstaStructure.get_bio(self.driver)
        
        if get_followers:
            user.followers_list = self.__get_list__(user)
            
        if get_following:
            user.following_list = self.__get_list__(user, which='following')
        
        if get_posts:
            self.__get_posts__(user=user)


    def get_into_subreddit(self, subreddit):
        search_bar = RedditStructure.get_search_input(self.driver)
        search_bar.send_keys(subreddit)
        search_bar.send_keys(Keys.ENTER)

        RedditStructure.sleep(10)
        # RedditStructure.get_communities_clickable(self.driver).click()
        # RedditStructure.sleep(3)
        # RedditStructure.get_subreddit_clickable(self.driver, subreddit).click()
        # RedditStructure.sleep(3)


    def search_for(self, search, sort_by='relevance', timeout=10):
        waiter = WebDriverWait(self.driver, timeout)
        search_bar = waiter.until(EC.element_to_be_clickable(RedditStructure.get_search_input(self.driver, find=False)))
        search_bar.clear()
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.ENTER)
        RedditStructure.sleep(10)

        # sort_by = waiter.until(EC.element_to_be_clickable(RedditStructure.get_sort_by_clickable(self.driver, find=False)))

    

    def get_all_posts(self, timeout=10):
        posts = RedditStructure.get_all_posts_clickable(self.driver)
        return list(posts)
    

    def prepare_post_for_scrapping(self):
        does_it_expand = lambda clickable: clickable.text == '[+]' or 'load more comment' in clickable.text

        expands = set(RedditStructure.get_all_expand_comments_clickable(self.driver))
        expandables = filter(map(does_it_expand, expands)) # '[+]' or 'load more comment'

        while expandables:
            for expandable in expandables:
                expandable.click()

            expands = set(RedditStructure.get_all_expand_comments_clickable(self.driver))
            expandables = filter(map(does_it_expand, expands)) # '[+]' or 'load more comment'        


    def get_post_comments(self):
        comments = RedditStructure.get_all_comments(self.driver)
        retrieve_data_from_comment = lambda comment: (
            RedditStructure.get_parent_from_comment(comment).text,
            RedditStructure.get_comment_itself_from_comment(comment).text
        )

        return list(map(retrieve_data_from_comment, comments))
            
    def batch_process(self, searches, posts_limit, comments_limit):
        log_name = datetime.datetime.now().strftime('%H_%M_%d_%m_%Y.log')
        
        with open(log_name, 'a', encoding="utf-8") as log:
            # for subreddit in subreddits:
            #     try:
            #         date_now = datetime.datetime.now().strftime('%H:%M of %m/%d/%Y')
            #         # self.get_into_subreddit(subreddit)
            #         # log.write(f"entered {subreddit} at {date_now}\n")
            #     except Exception as ex:
            #         log.write(f"failed entering {subreddit} at {date_now} ({str(ex)})\n")
                
            for search in searches:
                try:
                    date_now = datetime.datetime.now().strftime('%H:%M of %m/%d/%Y')
                    self.search_for(search)
                    log.write(f"searched for {search} at {date_now}\n")

                    posts = self.get_all_posts()
                    
                    while posts and posts_limit > 0:
                        posts_limit -= 1
                        post_clickable = posts.pop()
                        url = self.driver.current_url
                        print(url)
                        # self.filter_by('new') # TODO
                        post_clickable.click()
                        title = RedditStructure.get_post_title(self.driver).text
                        print(title)
                        # post_date = RedditStructure.get_post_date(self.driver) # TODO
                        # post_upvotes = RedditStructure.get_post_upvotes(self.driver) # TODO
                        try:
                            post_itself = RedditStructure.get_post_itself(self.driver).text
                        except:
                            post_itself = ''
                        post_data = Post(url, title, post_itself)

                        self.prepare_post_for_scrapping()
                        post_data.comments = self.get_post_comments()

                except Exception as ex:
                    log.write(f"failed searching for {search} at {date_now} ({str(ex)})\n")
