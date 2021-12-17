import scrapy
import imdb
import re
from scrapy.item import Item, Field

#TODO:
#scrapy log exporting
#runtime, failures, etc
#test run

#TODO: cleaner

numbClean = re.compile(r'\d+(?:\.\d+)?')
ia = imdb.IMDb()
genre_list = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Superhero', 'Thriller', 'War', 'Western']

class ImdbScraperItem(scrapy.Item):
    rank = scrapy.Field()
    movieId = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    votes = scrapy.Field()
    runtime = scrapy.Field()
    genres = scrapy.Field()
    plot = scrapy.Field()
    actors = scrapy.Field()
    writers = scrapy.Field()
    directors = scrapy.Field()
    producers = scrapy.Field()
    companies = scrapy.Field()
    url = scrapy.Field()
    pass


class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = []
    for genre in genre_list:
            base_url = f'https://www.imdb.com/search/title/?genres={genre}&explore=title_type,genres&title_type=movie&ref_=adv_explore_rhs'
            start_urls.append(base_url.format(genre))    

    def parse(self, response):
        #outer movie containers
        everyContainer = response.xpath('//*[@class="lister-item mode-advanced"]')
        #for container in genre grab their rank, then meta data
        for container in everyContainer:
            item = ImdbScraperItem()
            #take "base genre" from URL. if ['blah blah'] in url
            item['url'] = response.request.url
            item['rank'] = container.xpath('./div/h3/span/text()').extract()[0].replace('.', '')
            #parse id from URL
            id = int(numbClean.findall(container.xpath('./div/h3/a/@href').extract()[0])[0])
            #use imdb to fetch 
            item['movieId'] = id
            movie = ia.get_movie(id)         
            item['title'] = movie.get('title')
            item['year'] = movie.get('year')
            item['rating'] = movie.get('rating')
            item['votes'] = movie.get('votes')
            item['runtime'] = movie.get('runtimes')
            item['genres'] = movie.get('genre')
            item['plot'] = movie.get('plot')
            cast = movie.get('cast')
            castList = []
            for actor in cast:
                actorTuple = (actor.get('name'), actor.personID)
                castList.append(actorTuple)
            item['actors'] = castList
            #check if writer is null, or double counted
            #if writer is not null and writer is not in set of writer names
            writers = movie.get('writer')
            writerList = []
            for writer in writers:
                writerTuple = (writer.get('name'), writer.personID)
                writerList.append(writerTuple)
            item['writers'] = writerList
            #handle multiple directors
            directors = movie.get('director')
            directorList = []
            for director in directors:
                directorTuple = (director.get('name'), director.personID)
                directorList.append(directorTuple)          
            item['directors'] = directorList
            #producers
            producers = movie.get('producer')
            producerList = []
            for producer in producers:
                producerTuple = (producer.get('name'), producer.personID)
                producerList.append(producerTuple)
            item['producers'] = producerList
            #production companies
            companies = movie.get('production companies')
            companyList = []
            for company in companies:
                companyTuple = (company.get('name'), company.companyID)
                companyList.append(companyTuple)
            item['companies'] = companyList
            yield item