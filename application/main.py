import threading

import qdarkstyle
from PyQt5 import QtWidgets
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from application.ui_window import Ui_MainWindow
from application.youtube_spider import YoutubeSpider


class CrawlerThread(threading.Thread):
    def __init__(self, link):
        super(CrawlerThread, self).__init__()
        self.link = link

    def run(self):
        crawler_runner = CrawlerRunner()
        crawler_runner.crawl(YoutubeSpider, self.link)

        reactor.run(installSignalHandlers=False)


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.extractButton.clicked.connect(self.extract_links)

    def extract_links(self):
        link = self.ui.linkEditLine.text()
        if len(link) > 0 and link.__contains__('youtube.com'):
            thread = CrawlerThread(link)
            thread.start()
        else:
            # raise Exception("INVALID LINK")
            print("INVALID LINK")


def main():
    app = QtWidgets.QApplication([])
    window = Window()
    window.show()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.exec_()


if __name__ == "__main__":
    main()
