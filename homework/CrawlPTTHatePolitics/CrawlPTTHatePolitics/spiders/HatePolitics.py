import scrapy
from scrapy.http import FormRequest
import logging
from CrawlPTTHatePolitics.items import PostItem
import datetime
from datetime import datetime

class HatePoliticsSpider(scrapy.Spider):
    name = 'HatePolitics'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/HatePolitics/index.html']

    _retries = 0
    MAX_RETRY = 1

    _pages = 0
    MAX_PAGES = 1000
    def parse(self, response):
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            if self._retries < HatePoliticsSpider.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                yield FormRequest.from_response(response, formdata={'yes': 'yes'}, callback=self.parse)
            else:
                logging.warning('you cannot pass')

        else:
            self._pages += 1
            for href in response.css('.r-ent > div.title > a::attr(href)')[0:-4]:
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_post)

            if self._pages < HatePoliticsSpider.MAX_PAGES:
                next_page = response.xpath('//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    logging.warning('follow {}'.format(url))
                    yield scrapy.Request(url, self.parse)
                else:
                    logging.warning('no next page')
            else:
                logging.warning('max pages reached')
    def parse_post(self, response):

        item = PostItem()
        item['url'] = response.url
        datetime_str = response.xpath('//div[@class="article-metaline"]/span[@class="article-meta-value"]/text()')[-1].extract()
        print(datetime_str)
        item['date'] = datetime.strptime(datetime_str, "%a %b %d %H:%M:%S %Y")
        # item['content'] = response.xpath('//div[@id="main-container"]/text()')
        # item['content'] = response.xpath('//div[@class="main-content"]/text()').get()
        # strcontent = repr()
        contentlist = response.xpath('//*[@id="main-content"]/text()[1]')
        for content in contentlist.extract():
            x = content.replace("\n", "").replace(" ", "").strip()
        item['content'] = x
        yield item
# //*[@id="main-content"]/text()[1]
