

from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TELEGRAM_TOKEN")
chat_ids = []

def load_chats():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    a = requests.get(url).json()
    global chat_ids
    for b in a["result"]:
        chat_ids.append(b['message']['chat']['id'])

    chat_ids = set(chat_ids)

    for b in chat_ids:
        print(b)

 


def main_loop():
    load_chats()
    driver = webdriver.Firefox()
    while True:
        driver.get("https://www.upwork.com/nx/jobs/search/?q=python&sort=recency")
        time.sleep(10)
        response = driver.page_source
        soup = BeautifulSoup(response, "html.parser")
        works = soup.find_all("section", attrs={"class":"up-card-section up-card-list-section up-card-hover"})
    
        for work in works:
            w_title = work.find("h3", attrs={"class":"my-0 p-sm-right job-tile-title"}).text
            w_tile = work.find("div", attrs={"data-test":"JobTileFeatures"}).text
            w_desc = work.find("span", attrs={"data-test":"job-description-text"}).text
            
            for chat_id in chat_ids:
                message = "<b>Title:</b>\t{}\n\n<b>Description:</b>\t{}\n\n<b>Additional Info:</b>\t{}".format(w_title, w_desc, w_tile)
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html"
                print(requests.get(url).json()) 
                time.sleep(1)
        time.sleep(600)


if __name__ == "__main__":
    main_loop()