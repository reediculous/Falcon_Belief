from scraper import BeliefSpider
from keywords import kwCheck, kwCheck1, keywords
from threading import Thread

class mainThread(Thread):
    def run(self):
        spider = BeliefSpider()
        spider.run(regime="main")

class sneakerThread(Thread):
    def run(self):
        spider = BeliefSpider()
        spider.run(regime="items")

if __name__ == '__main__':
    mt = mainThread()
    sn = sneakerThread()
    mt.start()
    sn.start()




