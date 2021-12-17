# imdb-etl

##To Use
Create the database
```
docker-compose up
```
Start the spider by navigating to imdb_initial_etl/scraper
```
scrapy crawl imdb_spider
```
Crawler will take some time (as there are no proxies). Afterwards, move the .csv.gz file to ./transformations and run cleaning.py
```
python3 cleaning.py
```

#Systems Architecture
![Unnamed File](https://user-images.githubusercontent.com/7442267/146496459-43987641-2148-4fa0-bbf8-7015acbd9021.png)
#ERD
![Database ER diagram (crow's foot)](https://user-images.githubusercontent.com/7442267/146496462-10315d9a-1863-47c9-ae9e-6bc0337cdbad.png)
