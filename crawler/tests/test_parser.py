""" This modules contains the test case for Parser"""

import unittest
from datetime import datetime

from crawler.parser import Parser

from core.constant import PROJECT_ROOT


class ParserTestCase(unittest.TestCase):
    "Test case for Parser modules"

    def setUp(self):
        pass

    def test_get_head_news_list(self):
        "test get head news list from test data"

        with open(PROJECT_ROOT + '/crawler/tests/web.html', 'r') as file:
            test_html = file.read()

        news_list = Parser.get_head_news_list(test_html)
        self.assertEqual(3, len(news_list))

    def test_get_new_detail(self):
        "test get news detail from test data"

        reference_title = "穿雷納德球衣「加持」？ 加拿大高球好手抓鳥失利"
        reference_datetime = "2019-06-07 17:36"
        reference_datetime_object = datetime.strptime(reference_datetime,
                                                      "%Y-%m-%d %H:%M")
        reference_content = "本周開打的PGA加拿大公開賽"
        with open(PROJECT_ROOT + '/crawler/tests/web_detail.html',
                  'r') as file:
            test_html = file.read()

        title, datetime_object, content = Parser.get_news_detail(test_html)

        self.assertEqual(reference_title, title)
        self.assertTrue(isinstance(datetime_object, datetime))
        self.assertEqual(reference_datetime_object, datetime_object)
        self.assertIn(reference_content, content)
