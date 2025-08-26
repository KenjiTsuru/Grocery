import playwright
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright, Playwright

class itemList:
    def __init__(self, name):
        self.name = name
        self.list = []
class Item:
    def __init__(self, name, store, price, deal):
        self.name = name
        self.store = store
        self.price = price
        self.deal = deal

def grabUrls(x):
    browser = p.chromium.launch()
    page = browser.new_page()
    url = ("https://flipp.com/search/" + x)
    page.goto(url)
    page.locator('//div[@class="item-container"]/div[@class="wrapper"]/a').first.wait_for(state="attached", timeout = 10000)
    urls = []
    handleLinks = page.locator('//div[@class="item-container"]/div[@class="wrapper"]/a')
    for links in handleLinks.element_handles():
        href_value = links.get_attribute('href')
        urls.append("https://flipp.com" + href_value)
    return urls

def grabItems():
    with open("example.txt") as f:
        for x in f:
            itemsList = itemList(x)
            browser = p.chromium.launch()
            page = browser.new_page()
            urls = grabUrls(x)
            for url in urls:
                page.goto(url)
                page.locator('//span[@content-slot="title"]').first.wait_for(state="attached", timeout=10000)
                name = page.locator('//span[@content-slot="title"]').first.inner_text()
                store = page.locator('//span[@class="subtitle"]').first.inner_text()

                try:
                    page.locator('//div[@class="item-price-info"]/flipp-price').first.wait_for(state="attached", timeout=200)
                    price = float(page.locator('//div[@class="item-price-info"]/flipp-price').get_attribute("value"))

                except:
                    price = 0

                try:
                    page.locator('//div[@class="sale-story"]').first.wait_for(state="attached", timeout=200)
                    deal = page.locator('//div[@class="sale-story"]').first.inner_text()

                except:
                    deal = "none"

                print("Name: " + name + " Store: " + store + " Price: " + str(price) + " Deal: " + deal)
                item = Item(name, store, price, deal)
                itemsList.list.append(item)
            groceryList.append(itemsList)

groceryList = []
with sync_playwright() as p:
    grabItems()

for i in range(len(groceryList)):
    groceryList[i].list.sort(key=lambda x: x.price)

for i in range(len(groceryList)):
    print(groceryList[i].name)
    for j in range(len(groceryList[i].list)):
        print("Name: " + groceryList[i].list[j].name + " Store: " + groceryList[i].list[j].store + " Price: " + str(groceryList[i].list[j].price) + " Deal: " + groceryList[i].list[j].deal)
