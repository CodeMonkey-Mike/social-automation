import scrapy
from scrapy.crawler import CrawlerProcess

class FinanceYahooArticleSpider(scrapy.Spider):
    name = 'finance_yahoo_article'
    allowed_domains = ['finance.yahoo.com']
    start_urls = []  # Initialize with an empty list

    def parse(self, response):
        # Extract the article title
        article_title = response.css('h1::text').get()

        # Extract the author (if available)
        author = response.css('span[class*="caas-author-byline-collapse"]::text').get()

        # Extract the article content
        article_content = response.css('div[class*="caas-body"] p::text').getall()
        article_content = ' '.join(article_content)

        # Create a dictionary to store the extracted data
        article_data = {
            'title': article_title,
            'author': author,
            'content': article_content,
            'url': response.url,
        }

        return article_data

def scrape_article(article_url):
    # Create a Scrapy CrawlerProcess
    process = CrawlerProcess()

    # Set the start_urls for the spider based on the provided article_url
    FinanceYahooArticleSpider.start_urls = [article_url]

    # Add the spider to the process
    process.crawl(FinanceYahooArticleSpider)

    # Start the crawling process
    process.start()

    # Retrieve the scraped data from the spider's output
    scraped_data = process.crawl(FinanceYahooArticleSpider).get('items')

    return scraped_data

