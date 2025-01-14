""" This modules contains the functions for scrape regulary """
import threading
import time

from core import base
from core.constant import INDEX_URL, PROJECT_ROOT, INTERVAL_TIME

from crawler.scraper import Scraper
from crawler.parser import Parser

from news.models import News


class CrawlerService():

    def __init__(self, url=None):
        self.url = url
        self.news_url_list = list()

    def request_head_news_list(self):
        news_list = list()

        scraper = Scraper(self.url)
        text = scraper.run()

        news_list = Parser.get_head_news_list(text)
        self.news_url_list = news_list

        return news_list

    def request_news(self, url):
        news = News()
        scraper = Scraper(url)
        text = scraper.run()

        title, datetime_object, content = Parser.get_news_detail(text)

        news.title = title
        news.created_at = datetime_object
        news.content = content
        news.url = url

        checked_news = News.objects.filter(title=title)
        if len(checked_news) == 0:
            news.save()

        return news

    def get_news(self, url=None):
        if url is None:
            news_list = list()
            for news_url in self.news_url_list:
                news = self.request_news(news_url)
                news_list.append(news)

            return news_list

        news = self.request_news(news_url)

        return news

    def run(self):
        self.request_head_news_list()
        news_list = self.get_news()

        return news_list

    def schdeuled_run(self):
        while True:
            print("HHHHHHHHHHHHH")
            self.run()
            time.sleep(INTERVAL_TIME)

    def threading_run(self):
        flag = 1
        for thread in threading.enumerate():
            if thread.name == "crawler_service_run":
                flag = 0
        if flag:
            t = threading.Thread(target=self.schdeuled_run, name="crawler_service_run")
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    crawler_service = CrawlerService(INDEX_URL)
    crawler_service.schdeuled_run()
