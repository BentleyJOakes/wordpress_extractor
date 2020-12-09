import scrapy


class WordpressSpider(scrapy.Spider):
    name = "wordpress"
    start_urls = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        if not WordpressSpider.start_urls:
            url = input("Enter URL: ")
            WordpressSpider.start_urls = [url]

        print("URLs: " + str(WordpressSpider.start_urls))
        for url in WordpressSpider.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for readmore in response.css('p.readmore'):
            link = readmore.css('a::attr(href)').get()

            yield response.follow(link, callback=self.article_parse)

        next_page = response.css('.nav-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def article_parse(self, response):
        title = response.css(".entry-title > a:nth-child(1)::text").get()
        date = response.css(".entry-date::text").get()
        author = response.css(".url::text").get()

        content = response.css(".entry-content").get()
        tags = response.css(".entry-utility a::text").getall()
        yield {
            'title': title,
            'date': date,
            'author': author,
            'content' : content,
            'tags' : tags
        }