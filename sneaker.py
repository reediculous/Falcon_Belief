class SneakerPreview():
    shop = "Belief"
    def __init__(self, link, name, image, price, sizes):
        self.__link = link
        self.__name = name
        self.__image = image
        self.__price = price
        self.__sizes = sizes

    def getLink(self):
        return self.__link

    def setLink(self, link):
        if not link is None:
            self.__link = link
        else:
            self.__link = "не удалось получить ссылку :("

    def getPrice(self):
        return self.__price

    def setPrice(self, price):
        if not price is None:
            self.__price = price
        else:
            self.__price = ""

    def getName(self):
        return self.__name

    def setName(self, name):
        if not name is None:
            self.__name = name
        else:
            self.__name = "Не удалось подгрузить название кроссовка"

    def getImage(self):
        return self.__image

    def setImage(self, image):
        if not image is None:
            self.__image = image
        else:
            self.__image = ""

    def getSizes(self):
        return self.__sizes

    def setSizes(self, sizes):
        self.__sizes = sizes

    def compileString(self):
        sizesList = ""
        for size in self.__sizes:
            sizesList += size + "\n"
        return str(self.__name) + "\n" + sizesList + str(self.__link) + "#droptop" + "\n"