BOT_NAME = 'blanja'
SPIDER_MODULES = ['blanja.spiders']
NEWSPIDER_MODULE = 'blanja.spiders'
ROBOTSTXT_OBEY = False
DEFAULT_REQUEST_HEADERS = {
    'Origin': 'https://www.blanja.com',
    'Referer': 'https://www.blanja.com/',
}
ITEM_PIPELINES = {
    'blanja.pipelines.BlanjaPipeline': 300,
}
CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8mb4".format(
    drivername="mysql",
    user="root",
    passwd="",
    host="localhost",
    port="3306",
    db_name="scrapy_blanja",
)

DOWNLOADER_MIDDLEWARES = {
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'blanja.middlewares.RotateUserAgentMiddleware': 543,
}
SPIDER_MIDDLEWARES = {

}
USER_AGENT_CHOICES = [
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
]
# ...
PROXY_LIST = 'proxies.txt'
PROXY_MODE = 0
CONCURRENT_ITEMS = 1000
CONCURRENT_REQUESTS = 1000
CONCURRENT_REQUESTS_PER_DOMAIN = 1000