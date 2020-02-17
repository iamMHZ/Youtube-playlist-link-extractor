import time
import webbrowser

import requests
import scrapy
from lxml import html
from scrapy.crawler import CrawlerProcess


class YoutubeSpider(scrapy.Spider):
    base_download_url = 'https://www.ssyoutube.com'
    name = "youtube"

    def __init__(self, *args, **kwargs):
        super(YoutubeSpider, self).__init__(*args, **kwargs)
        self.link = args[0]

    def start_requests(self):
        yield scrapy.Request(url=self.link, callback=self.parse)

    def parse(self, response):
        print("\n\n\n\n######################################################################")

        links = response.css('a::attr(href)').extract()
        # removing repetitive links by converting list to set
        links = set(links)
        for link in links:
            if str(link).__contains__('index'):
                # print(link)

                download_page_link = YoutubeSpider.base_download_url + link
                # open download link in default browser
                self.open_link_in_browser(download_page_link)

                print(download_page_link)
                self.write_to_file(download_page_link)

                # self.crawl_inside_download_page(download_page_link)

        print("\n\n\n\n######################################################################")

    def open_link_in_browser(self, link):
        # opening link in default browser
        webbrowser.open(link, new=2)
        #  waiting until current page loads in browser
        time.sleep(5)

    def crawl_inside_download_page(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)
        download_links = tree.xpath('//a[@class]/text()')
        # titles = tree.cssselect('a::attr(title)')

        for dl in download_links:
            print(dl)

            self.write_to_file(dl)

    def write_to_file(self, text):
        f = open("links.txt", "a")
        f.write(str(text.encode('utf-8')) + '\n')
        f.close()
    # container > h1 > yt-formatted-string


def extract_links(link):
    process = CrawlerProcess()
    process.crawl(YoutubeSpider, link)
    process.start()

# link = 'https://www.youtube.com/watch?v=EeFqcmaw6iA&list=PL7u4lWXQ3wfKqFjzTSBmylEeVP9ibx_XT'
# extract_links(link)
