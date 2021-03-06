import time
import webbrowser

import requests
import scrapy
from lxml import html
from scrapy.crawler import CrawlerProcess


class YoutubeSpider(scrapy.Spider):
    download_link_prefix = 'https://www.ssyoutube.com'
    youtube_link_prefix = 'https://www.youtube.com'
    file_name = 'links.txt'

    name = "youtube"

    def __init__(self, *args, **kwargs):
        super(YoutubeSpider, self).__init__(*args, **kwargs)
        self.start_url = args[0]

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        print('\n\n\n\n')
        print("".rjust(70, '#'))

        links = response.css('a::attr(href)').extract()
        # removing repetitive links by converting list to set
        links = set(links)

        links = self.extract_playlist_links(links)
        # links are sored based on their playlist order:
        links = sorted(links, key=lambda l: int(str(l).split('=')[-1].strip()))

        # open and save links
        for link in links:
            # print(link)

            download_page_link = YoutubeSpider.download_link_prefix + link
            youtube_page_link = YoutubeSpider.youtube_link_prefix + link

            # open download link in default browser
            self.open_link_in_browser(download_page_link)

            print(download_page_link)
            self.write_to_file('YOUTUBE : ' + youtube_page_link)
            self.write_to_file('DOWNLOAD : ' + download_page_link)
            self.write_to_file("")

            # self.crawl_inside_download_page(download_page_link)

        print(" \n\n\n\n".rjust(70, '#') + "\n\n\n\n")

    def extract_playlist_links(self, links):
        palylist_links = []

        # filter other links:
        for link in links:

            if str(link).__contains__('index') and str(link).__contains__('watch') and not str(link).__contains__(
                    'https'):
                palylist_links.append(link)

        return palylist_links

    def open_link_in_browser(self, link):
        # opening link in default browser
        webbrowser.open(link, new=2)
        #  waiting until current page loads in browser
        time.sleep(3)

    def crawl_inside_download_page(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)
        download_links = tree.xpath('//a[@class]/text()')
        # titles = tree.cssselect('a::attr(title)')

        for dl in download_links:
            print(dl)

            self.write_to_file(dl)

    def write_to_file(self, text):
        f = open(YoutubeSpider.file_name, "a")
        f.write(str(text) + '\n')
        f.close()
    # container > h1 > yt-formatted-string


def extract_links(link):
    process = CrawlerProcess()
    process.crawl(YoutubeSpider, link)
    process.start()


if __name__ == '__main__':

    link = 'https://www.youtube.com/watch?v=EeFqcmaw6iA&list=PL7u4lWXQ3wfKqFjzTSBmylEeVP9ibx_XT'
    extract_links(link)
