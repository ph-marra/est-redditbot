from driver import RedditDriver
from bot import RedditBot

# subreddits = ['brasilivre']
searches = ["subreddit:brasilivre preto"]
# searches = ['preto', 'negro']
posts_limit = 1
comments_limit = 10

driver = RedditDriver('pedrohenriquemarraarajo1@gmail.com', 'ajG7wkvT6$') # insert username and password
driver.mount_driver('chromedriver.exe')
driver.login()

bot = RedditBot(driver)

bot.batch_process(searches, posts_limit, comments_limit)