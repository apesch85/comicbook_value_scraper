import re
import time
from typing import Any, Optional, List
from dataclasses import dataclass

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common import exceptions as selenium_e




@dataclass
class Web:
    driver: webdriver.Chrome
    url: str

    def connect(self, search, issue):
        self.driver.get(self.url)
        issue_elem = self.driver.find_element(By.ID, "issueNu")
        issue_elem.clear()
        issue_elem.send_keys(issue)
        elem = self.driver.find_element(By.ID, "search")
        elem.clear()
        elem.send_keys(search)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
    
    def find_issue(self, year):
        issues = self.driver.find_elements(
            By.XPATH, 
            "//td[@class='col-5 sm-line-height']")
        print("Issues found: %s" % len(issues))
        # /[@class='grid_issue_info']/span"
        for issue in issues:
            metadata = issue.find_element(By.CLASS_NAME, "grid_issue_info")
            if re.search(str(year), metadata.text):
                issue_link = issue.find_element(
                    By.CLASS_NAME, 
                    "grid_issue").get_attribute('href')
                return issue_link
        return ""

    def open_link(self, link):
        self.driver.get(link)

    def authenticate(self, username, passowrd):
        pass


@dataclass  
class Comic(Web):

    username: str
    password: str
    title: str
    issue: int
    year: int


    def get(self):
        self.connect(self.title, self.issue)
        self.issue_link = self.find_issue(self.year)
        if self.issue_link:
            self.open_link(self.issue_link)
            time.sleep(30)

@dataclass
class rating:
    graded_9: Optional[str]
    ungraded_9: Optional[str]
    graded_8: Optional[str]
    ungraded_8: Optional[str]
    graded_7: Optional[str]
    ungraded_7: Optional[str]
    graded_6: Optional[str]
    ungraded_6: Optional[str]
    graded_5: Optional[str]
    ungraded_5: Optional[str]
    graded_4: Optional[str]
    ungraded_4: Optional[str]
    graded_3: Optional[str]
    ungraded_3: Optional[str]
    graded_2: Optional[str]
    ungraded_2: Optional[str]
    graded_1: Optional[str]
    ungraded_1: Optional[str]