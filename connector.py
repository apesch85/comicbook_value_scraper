import re
import time
from typing import Any, Optional, List
from dataclasses import dataclass, field

from bs4 import BeautifulSoup
import gspread
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
        print("Issues found on comicspriceguide: %s" % len(issues))
        for issue in issues:
            metadata = issue.find_element(By.CLASS_NAME, "grid_issue_info")
            if re.search(str(year), metadata.text):
                print('Issue with matching year: %s found!' % year)
                issue_link = issue.find_element(
                    By.CLASS_NAME, 
                    "grid_issue").get_attribute('href')
                return issue_link
        return ""

    def open_link(self, link):
        self.driver.get(link)

    def login_page_exists(self):
        try:
            self.driver.find_element(
                By.XPATH, 
                "//div[@class='alert p-0 m-0 border border-dark rounded ']")
            return True
        except selenium_e.NoSuchElementException:
            return False

    def login(self, username, password):
        self.driver.find_element(By.XPATH, '//a[@href="/login"]').click()
        user_field = self.driver.find_element(By.ID, 'user_username')
        password_field = self.driver.find_element(By.ID, 'user_password')
        login_button = self.driver.find_element(By.ID, 'btnLogin')
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        password_field.send_keys(password)
        login_button.click()
        time.sleep(15)
        self.driver.back()
        self.driver.refresh()

    def get_value(self, username=None, password=None):
        self.driver.find_element(By.ID, 'values-tab').click()
        r = re.compile('\d+')
        if self.login_page_exists():
            print('Login page detected. Logging in...')
            self.login(username, password)
        
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, features='html.parser')
        found = soup.find_all('td', class_='f-10')
        ratings = [rating for rating in found if 'Graded values do not' not in rating.get_text()]
        comic_ratings = Rating()
        for rating in ratings:
            rate_val = int(r.search(rating.get_text()).group(0))
            if rate_val == 10:
                comic_ratings.ungraded_10 = rating.find_next('td').text.strip()
                comic_ratings.graded_10 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 9:
                comic_ratings.ungraded_9 = rating.find_next('td').text.strip()
                comic_ratings.graded_9 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 8:
                comic_ratings.ungraded_8 = rating.find_next('td').text.strip()
                comic_ratings.graded_8 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 7:
                comic_ratings.ungraded_7 = rating.find_next('td').text.strip()
                comic_ratings.graded_7 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 6:
                comic_ratings.ungraded_6 = rating.find_next('td').text.strip()
                comic_ratings.graded_6 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 5:
                comic_ratings.ungraded_5 = rating.find_next('td').text.strip()
                comic_ratings.graded_5 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 4:
                comic_ratings.ungraded_4 = rating.find_next('td').text.strip()
                comic_ratings.graded_4 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 3:
                comic_ratings.ungraded_3 = rating.find_next('td').text.strip()
                comic_ratings.graded_3 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 2:
                comic_ratings.ungraded_2 = rating.find_next('td').text.strip()
                comic_ratings.graded_2 = rating.find_next('td').find_next('td').text.strip()
            elif rate_val == 1:
                comic_ratings.ungraded_1 = rating.find_next('td').text.strip()
                comic_ratings.graded_1 = rating.find_next('td').find_next('td').text.strip()

        return comic_ratings

@dataclass
class Rating:
    graded_10: Optional[str] = None
    ungraded_10: Optional[str] = None
    graded_9: Optional[str] = None
    ungraded_9: Optional[str] = None
    graded_8: Optional[str] = None
    ungraded_8: Optional[str] = None
    graded_7: Optional[str] = None
    ungraded_7: Optional[str] = None
    graded_6: Optional[str] = None
    ungraded_6: Optional[str] = None
    graded_5: Optional[str] = None
    ungraded_5: Optional[str] = None
    graded_4: Optional[str] = None
    ungraded_4: Optional[str] = None
    graded_3: Optional[str] = None
    ungraded_3: Optional[str] = None
    graded_2: Optional[str] = None
    ungraded_2: Optional[str] = None
    graded_1: Optional[str] = None
    ungraded_1: Optional[str] = None

@dataclass  
class Comic(Web):

    username: str
    password: str
    title: str
    issue: int
    year: int
    issue_link: Optional[str] = None
    graded_10: Optional[Rating.graded_10] = None
    graded_9: Optional[Rating.graded_9] = None
    graded_8: Optional[Rating.graded_8] = None
    graded_7: Optional[Rating.graded_7] = None
    graded_6: Optional[Rating.graded_6] = None
    graded_5: Optional[Rating.graded_5] = None
    graded_4: Optional[Rating.graded_4] = None
    graded_3: Optional[Rating.graded_3] = None
    graded_2: Optional[Rating.graded_2] = None
    graded_1: Optional[Rating.graded_1] = None
    ungraded_10: Optional[Rating.ungraded_10] = None
    ungraded_9: Optional[Rating.ungraded_9] = None
    ungraded_8: Optional[Rating.ungraded_8] = None
    ungraded_7: Optional[Rating.ungraded_7] = None
    ungraded_6: Optional[Rating.ungraded_6] = None
    ungraded_5: Optional[Rating.ungraded_5] = None
    ungraded_4: Optional[Rating.ungraded_4] = None
    ungraded_3: Optional[Rating.ungraded_3] = None
    ungraded_2: Optional[Rating.ungraded_2] = None
    ungraded_1: Optional[Rating.ungraded_1] = None


    def get(self):
        self.connect(self.title, self.issue)
        self.issue_link = self.find_issue(self.year)
        if self.issue_link:
            self.open_link(self.issue_link)
            time.sleep(5)
            ratings = self.get_value(self.username, self.password)
            self.graded_10 = ratings.graded_10
            self.graded_9 = ratings.graded_9
            self.graded_8 = ratings.graded_8
            self.graded_7 = ratings.graded_7
            self.graded_6 = ratings.graded_6
            self.graded_5 = ratings.graded_5
            self.graded_4 = ratings.graded_4
            self.graded_3 = ratings.graded_3
            self.graded_2 = ratings.graded_2
            self.graded_1 = ratings.graded_1
            self.ungraded_10 = ratings.ungraded_10
            self.ungraded_9 = ratings.ungraded_9
            self.ungraded_8 = ratings.ungraded_8
            self.ungraded_7 = ratings.ungraded_7
            self.ungraded_6 = ratings.ungraded_6
            self.ungraded_5 = ratings.ungraded_5
            self.ungraded_4 = ratings.ungraded_4
            self.ungraded_3 = ratings.ungraded_3
            self.ungraded_2 = ratings.ungraded_2
            self.ungraded_1 = ratings.ungraded_1

@dataclass
class Speadsheet:

    sheet: gspread.worksheet.Worksheet
    unprocessed: Optional[List[List[str]]] = field(default_factory=list)
    processed: Optional[List[List[str]]] = field(default_factory=list)

    def parse_sheet(self):
        if len(self.sheet.get_values()[1:]) == 0:
            return False
        for i, row in enumerate(self.sheet.get_values()[1:]):
            if row[3] != "Scraped":
                row.append(i + 2)
                self.unprocessed.append(row)
            else:
                self.processed.append(row)
        print('Number of unprocessed comics: %d' % len(self.unprocessed))
        print('Number of processed comics: %d' % len(self.processed))
        return True

    def update_sheet(self, row):
        r_idx = row[-1]
        row.pop()
        row[3] = "Scraped"
        self.sheet.update('A%s:Y%s' % (r_idx, r_idx), [row])
        time.sleep(1)
        print('Finished adding comic to sheet!')

