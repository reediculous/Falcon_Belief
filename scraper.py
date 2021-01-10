import time
from urllib import request
import disInterface
import discord
from bs4 import BeautifulSoup
from sneaker import SneakerPreview
from database import sqlInterface
import json
from random import shuffle


class BeliefSpider:
    # Реализует получение информации о кроссовках из магазина beliefmoscow
    # Класс работает со списком ссылок на страницы кроссовок links

    start_url = "https://beliefmoscow.com/collection/obuv"
    links = []
    config = {
        'user': 'root',
        'password': '1$gptSINGLE<PYJRTD',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'Falcon',
        'auth_plugin': 'mysql_native_password',
        'raise_on_warnings': True,
    }
    sql = sqlInterface(config)

    whToken = "R6ju280blyKDX0uDNZY9vqZCU5rfabnaVko1pXRqsFaH3vUpUpg9z6X5_xNQ5OAHSijT"
    webhook_mine = discord.Webhook.partial(754438355483361340, whToken,
                                           adapter=discord.RequestsWebhookAdapter())
    whToken2 = "3pICtn1ro6V3kAeEGS7bs074jfXc3Nyx6VnY-M0yeY9PjVCJWesYbdePO1uk7ubB6uJo"
    webhook_dt = discord.Webhook.partial(693559291352973462, whToken2,
                                         adapter=discord.RequestsWebhookAdapter())

    # Инициализируем экземляр класса для отправки сообщений в дискорд со списком вебхуков
    whInterface = disInterface.DiscordInterface([webhook_mine, webhook_dt])

    def __init__(self):
        self.current_url = self.start_url  # current_url — ссылка на текущую страницу с продуктами

    def parseMainPage(self):
        """
        Для главной страницы с товарами возвращает словарь, где:
        Ключ — наименование кроссовка
        Значение — экземпляр класса SneakerPreview, содержащий информацию о кроссовке
        """
        sneakers = {}
        if self.current_url != self.start_url:
            return
        try:
            response = request.urlopen(self.current_url)
            html = response.read().decode()
        except BaseException:
            return {}
        soup = BeautifulSoup(html, "html.parser")
        products = soup.select(".product_preview")
        for product in products:
            title = product.select_one(".product_preview-link")
            name = title.text
            name = name.replace("\n", "")
            name = name.replace("\t", "")  # TODO: удалить лишние пробелы
            name = name.strip()
            image = product.select_one(".product_preview-image")
            link = image['href']
            image = image.select_one(".image-dynamic-src")['src']  # Ссылка на фотографию продукта
            price = product.select_one(".product_preview-prices")  # TODO: обработать наличие двух цен
            price = price.text.replace("\n", "")
            price = price.strip()  # Цена кроссовка
            sneakers[name] = SneakerPreview("https://beliefmoscow.com" + link, name, image, price, [])
        return sneakers

    def parsePage(self):
        """
        Для второй и последующих страниц с товарами возвращает словарь, где:
        Ключ — наименование кроссовка
        Значение — экземпляр класса SneakerPreview, содержащий информацию о кроссовке
        """
        sneakers = {}
        try:
            response = request.urlopen(self.current_url)
            jsonData = json.load(response)
        except BaseException:
            return {}
        products = jsonData['products']
        for product in products:
            name = product['title']
            linkPrefix = product['url']
            link = "https://beliefmoscow.com" + linkPrefix
            sneakers[name] = SneakerPreview(link, name, "", "", [])
        return sneakers

    def shiftURL(self, back=False):
        """
        Переходит на следующую страницу, либо возвращается на стартовую
        """
        if back:
            self.current_url = self.start_url
            return
        if self.current_url == self.start_url:
            self.current_url = self.current_url + ".json?page_size=32&page=2"
        else:
            endPoint = self.current_url.rfind("=")
            pageNum = int(self.current_url[endPoint + 1:len(self.current_url):1])
            self.current_url = self.current_url[0:endPoint + 1:1] + str(pageNum + 1)

    def parseSneakerPage(self, link):
        """
        Для переданного адреса страницы с товаром возвращает экземпляр класса SneakerPreview,
        содержащий информацию о кроссовке.
        """
        try:
            response = request.urlopen(link)
            html = response.read().decode()
        except BaseException:
            return SneakerPreview(None, None, "", None, [])
        soup = BeautifulSoup(html, "html.parser")
        title = soup.select(".product-page__title")
        try:
            brand = title[0].text
            brand = brand.replace("\n", "")  # Наименование бренда
        except BaseException:
            brand = ""
        try:
            name = title[1].text
            name = name.replace("\n", "")
            name = name.replace("\t", "")
            name = name.strip()  # Наименование кроссовка
        except BaseException:
            name = ""
        try:
            sizesHtml = soup.select_one(".product-page__size")
            sizesHtml = sizesHtml.select("option")
            sizes = []
            for s in sizesHtml:
                sizes.append(s.text)  # Список строк — размеров кроссовка
        except BaseException:
            sizes = []
        try:
            price = soup.select_one(".product-page__price").text
            price = price.replace("\n", "")
            price = price.strip()  # Цена кроссовка
        except BaseException:
            price = None
        try:
            image = soup.select_one(".product-gallery-item")
            image = image.select_one("img")['src']  # Ссылка на изображение кроссовка
        except BaseException:
            image = ""
        return SneakerPreview(link, brand + " " + name, image, price, sizes)

    def run(self, regime="main"):
        """
        При режиме "main":
        В цикле проходит по всем страницам с кроссовками, собирая о них информацию.
        Если в итерации появляется кроссовок, которого не было в прошлой итерации, и если этот
        наименование кроссовка содержит одно из ключевых слов, то добавляет ссылку на кроссовок
        в список ссылок.
        ============================================
        При режиме "items":
        В цикле проходит по всем страницам из списка ссылок, собирая информацию о кроссовках.
        Если список размеров как-либо отличается от списка размеров на прошлой итерации, то
        отправляет информацию об этом в дискорд по всем указанным вебхукам.
        ============================================
        """
        if regime == "main":
            previews = {}
            spider = BeliefSpider()
            while 1:
                time.sleep(15)
                links = self.sql.pull("beliefurls")
                result = {}
                if previews == {}:
                    previews = result
                temp = spider.parseMainPage()
                if temp is not None:
                    result.update(temp)
                while temp != {}:
                    spider.shiftURL()
                    temp = spider.parsePage()
                    result.update(temp)
                for sneaker in result:
                    if not sneaker in previews and not result[sneaker].getLink() in links:
                        self.sql.push("beliefurls", result[sneaker].getLink())
                        print("added", result[sneaker].getLink(), "to database")
                if result != {}:
                    previews = result

        elif regime == "items":
            previous = {}
            isFirst = True
            while 1:
                time.sleep(3)
                links = self.sql.pull("beliefurls")
                shuffle(links)
                for link in links:
                    time.sleep(1)
                    sneaker = self.parseSneakerPage(link)
                    if not sneaker.getName() in previous:
                        if not isFirst and sneaker.getSizes() != []:
                            self.whInterface.send_embed(sneaker)
                        previous[sneaker.getName()] = sneaker
                    else:
                        if previous[sneaker.getName()].getSizes() != sneaker.getSizes():
                            if sneaker.getSizes() != []:
                                self.whInterface.send_embed(sneaker)
                            previous[sneaker.getName()] = sneaker
                isFirst = False
