import requests
from urllib.parse import urljoin
from multiprocessing.pool import ThreadPool, Pool
from bs4 import BeautifulSoup
from selenium import webdriver
import threading
import time
def get_links(link):
  res = requests.get(link)
  soup = BeautifulSoup(res.text,"lxml")
  titles = [str(urljoin(url,items.get("href"))) for items in soup.select(".question-hyperlink")]
  return titles

threadLocal = threading.local()

def get_driver():
  driver = getattr(threadLocal, 'driver', None)
  if driver is None:
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(options=chromeOptions)
    setattr(threadLocal, 'driver', driver)
  return driver


def get_title(url):
  driver = get_driver()
  driver.get(url)
  sauce = BeautifulSoup(driver.page_source,"lxml")
  item = sauce.select_one("h1 a").text
  print(item)

if __name__ == '__main__':
  url = "https://stackoverflow.com/questions/tagged/web-scraping"
ThreadPool(100).map(get_title, get_links(url))