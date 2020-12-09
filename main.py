import argparse

from scrapy.crawler import CrawlerProcess

from WordpressSpider import WordpressSpider
from scrapy.utils.project import get_project_settings

class WordPressExtractor:

    def __init__(self):
        self.process = CrawlerProcess(get_project_settings())

    def parse(self, start_urls):
        for surl in start_urls:
            WordpressSpider.start_urls = [surl]
            self.process.crawl(WordpressSpider, domain = surl)
            self.process.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] URL",
        description="Extract a WordPress site to HTML."
    )
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    wpe = WordPressExtractor()
    wpe.parse(list(args.files))
