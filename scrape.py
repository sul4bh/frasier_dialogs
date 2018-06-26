"""
Responsibility:
* Use webdriver to fetch a episode webpage
* DOM manipulation/selection
* Use `parse` to extract data that cannot be fetched using trivial regular expressions
"""

import re

from .parse import *


class Scrape(object):
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        
        self.driver.get(self.url)

    def _get_value(self, regex, selector):
        lines = self.driver.find_element_by_css_selector(
            selector).text.split("\n")
        for line in lines:
            match = re.match(
                regex,
                line,
                re.MULTILINE | re.DOTALL
            )
            if match:
                return match.group(1).strip()

    def _get_transcript(self):
        probably_transripts = self.driver.find_elements_by_css_selector('pre')
        for element in probably_transripts:
            for sibling in element.find_elements_by_xpath('preceding-sibling::h2'):
                if re.search('transcript \{.*\}', sibling.text.lower()):
                    return element.text

    def get_episode_info(self):
        season = self._get_value(
            '^\[(\d+)\.\d+\]',
            'h1'
        )
        episode = self._get_value(
            '^\[\d+\.(\d+)\]',
            'h1'
        )
        title = self._get_value(
            '\[.*\](.*)',
            '#rightCol h1'
        )
        written_date = self._get_value(
            'Transcript written on (.*)',
            '#rightCol pre'
        )
        revised_date = self._get_value(
            'Transcript revised on (.*)',
            '#rightCol pre'
        )
        aired_date = self._get_value(
            'Original Airdate on NBC: (.*)',
            '#rightCol pre'
        )
        writers, director = get_director_and_writers(
            self.driver.find_element_by_css_selector('#rightCol pre').text
        )
        
        return {
            "season": season,
            "episode": episode,
            "title": title,
            "written_date": written_date,
            "revised_date": revised_date,
            "aired_date": aired_date,
            "writers": writers,
            "director": director
        }

    def get_dialog_info(self):
        return get_cast_dialog(self._get_transcript())
