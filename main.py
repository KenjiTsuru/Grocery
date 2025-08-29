import asyncio
import threading
import smtplib

from playwright.async_api import async_playwright
from email.message import EmailMessage

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

"""def removeDupes(list):
    record = set()
    res = []
    for i in list:
        for j in list.list:
            if list[i][j].name not in record:
                record.add(list[i][j].name)
                res.append(list[i][j])
    return res"""
def sendEmail(out):
    msg = EmailMessage()
    msg['Subject'] = 'This weeks flyer deals'
    msg['From'] = 'kenycomeau46@gmail.com'
    msg['To'] = 'kenycomeau16@gmail.com'
    msg.set_content(out)
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login('kenycomeau46@gmail.com', 'gtrv ugcs tppm ybyx')
    s.send_message(msg)
    s.quit()


def runGrabItems(x):
    asyncio.run(grabItems(x))
async def grabUrls(x):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        url = ("https://flipp.com/search/" + x)
        await page.goto(url)
        await page.locator('//div[@class="item-container"]/div[@class="wrapper"]/a').first.wait_for(state="attached", timeout = 10000)
        urls = []
        handleLinks = page.locator('//div[@class="item-container"]/div[@class="wrapper"]/a')
        for links in await handleLinks.element_handles():
            href_value = await links.get_attribute('href')
            urls.append("https://flipp.com" + href_value)
        await browser.close()
        return urls

async def grabItems(x):
    async with async_playwright() as p:
            itemsList = itemList(x)
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            urls = await grabUrls(x)
            record = set()
            for url in urls:
                await page.goto(url)
                await page.locator('//span[@content-slot="title"]').first.wait_for(state="attached", timeout=10000)
                name = await page.locator('//span[@content-slot="title"]').first.inner_text()
                store = await page.locator('//span[@class="subtitle"]').first.inner_text()

                try:
                    await page.locator('//div[@class="item-price-info"]/flipp-price').first.wait_for(state="attached", timeout=200)
                    price = float(await page.locator('//div[@class="item-price-info"]/flipp-price').get_attribute("value"))

                except:
                    price = 0

                try:
                    await page.locator('//div[@class="sale-story"]').first.wait_for(state="attached", timeout=200)
                    deal = await page.locator('//div[@class="sale-story"]').first.inner_text()

                except:
                    deal = "none"

                print("Name: " + name + " Store: " + store + " Price: " + str(price) + " Deal: " + deal)
                item = Item(name, store, price, deal)
                if item.name not in record:
                    record.add(item.name)
                    itemsList.list.append(item)
            groceries.append(itemsList)
            await browser.close()

groceries = []

if __name__ == "__main__":
    threads = []
    with open("example.txt") as f:
        for x in f:
            thread = threading.Thread(target=runGrabItems, args=(x,))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

for i in range(len(groceries)):
    groceries[i].list.sort(key=lambda x: x.price)

out = ""
for i in range(len(groceries)):
    print(groceries[i].name)
    out = out + "\n" + groceries[i].name + "\n"
    for j in range(len(groceries[i].list)):
        print("PRODUCT NAME: " + groceries[i].list[j].name + " STORE NAME: " + groceries[i].list[j].store + " PRODUCT PRICE: " + str(groceries[i].list[j].price) + " DEAL ATTACHED: " + groceries[i].list[j].deal)
        out = out + "PRODUCT NAME: " + groceries[i].list[j].name + " STORE NAME: " + groceries[i].list[j].store + " PRODUCT PRICE: " + str(groceries[i].list[j].price) + " DEAL ATTACHED: " + groceries[i].list[j].deal + "\n"

sendEmail(out)