"""
Responsibility:
* Find out transcript urls and fetch them with a time delay

- Why serial execution instead of ThreadPool/async etc?
We can afford to take it easy with crawling. Lets not choke the
web server or get ourselves blocked by the website operator.
Also, code is much simpler and requires less StackOverflow-ing.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback
import time
import random
import logging

from .scrape import Scrape
from .database import Database


class Crawl(object):
    started = "STARTED"
    error = "ERROR"
    completed = "COMPLETED"

    def __init__(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.url = url

        logging.info("Fetching {}.".format(self.url))
        self.driver.get(self.url)

    def _get_all_episodes(self):
        elems = self.driver.find_elements_by_css_selector(".SeasonList li a")
        episodes = [elem.get_attribute('href') for elem in elems]
        return episodes
    
    def pause(self):
        seconds = random.randint(10, 20)
        logging.info("Sleeping for {} seconds...".format(seconds))
        time.sleep(seconds)
    
    def run(self):
        for episode_url in self._get_all_episodes():
            database = Database()
            if database.check_history(episode_url, self.completed):
                continue
            else:
                database.save_history(episode_url, "", self.started)
            self.pause()
            try:
                scrape = Scrape(self.driver, episode_url)
                database.save_episode_info(episode_url, scrape.get_episode_info())
                for dialog in scrape.get_dialog_info():
                    database.save_script(episode_url, dialog['cast'], dialog['dialog'])

                database.save_history(episode_url, "", self.completed)
                logging.info("{}: {}".format(episode_url, self.completed))
            except Exception as e:
                logging.error("{}: {}".format(episode_url, self.error))
                logging.info(traceback.format_exc())
                database.save_history(episode_url, traceback.format_exc(), self.error)
