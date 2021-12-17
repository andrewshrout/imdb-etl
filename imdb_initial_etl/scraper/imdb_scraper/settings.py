# Scrapy settings for imdb_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy_gzip_exporters import FEED_EXPORTERS

BOT_NAME = 'imdb_scraper'

SPIDER_MODULES = ['imdb_scraper.spiders']
NEWSPIDER_MODULE = 'imdb_scraper.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'

ROBOTSTXT_OBEY = False

FEED_URI = '%(time)s--imdb_scrape.csv.gz'
FEED_FORMAT = 'csv.gz'
FEED_EXPORT_FIELDS = ['movieId', 'title', 'rank', 'year', 'plot', 'rating', 'votes', 'url', 'runtime', 'genres', 'cast', 'writers', 'directors', 'producers', 'companies']

LOG_FILE = 'scrape_log--%(time)s.txt'
#Put Email here to receive stats log
STATSMAILER_RCPTS = ['paul.g@haystacks.ai']

#PROXIES
#proxy stuff
#REACTOR_THREADPOOL_MAXSIZE = 15
#DOWNLOAD_TIMEOUT = 30

#https://github.com/TeamHG-Memex/scrapy-rotating-proxies 
#sourced from free-proxy-list.net
#PREFERRED: STORMPROXIES https://help.stormproxies.com/knowledge-base/start-using-storm-proxies/
#ROTATING_PROXY_LIST = [
#'177.87.168.6', '206.253.164.122', '46.4.96.137', '194.5.193.183', '199.19.226.12', '34.138.225.120', '74.141.186.101', '185.193.18.62', '206.253.164.120', '206.253.164.110', '206.253.164.101', '206.253.164.108', '199.19.225.250',
#"91.107.6.115", "37.232.183.74", "103.11.106.69", "190.152.5.17", "195.14.114.33", "45.63.58.90", "103.73.74.22", "45.128.220.48", "37.57.38.133", "78.157.225.216", "54.37.160.88", "190.196.176.5", "178.47.141.85"
#]

DOWNLOADER_MIDDLEWARES = {
    #'scrapy_crawl_once.CrawlOnceMiddleware': 50,
#    'rotating_proxies.middlewares.RotatingProxyMiddleware':610,
#    'rotating_proxies.middlewares.BanDetectionMiddleware':620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    }


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'imdb_scraper.middlewares.ImdbScraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'imdb_scraper.middlewares.ImdbScraperDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'imdb_scraper.pipelines.ImdbScraperPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
