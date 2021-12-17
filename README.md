# imdb-etl

## To Use
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

# Systems Architecture
![Unnamed File](https://user-images.githubusercontent.com/7442267/146496459-43987641-2148-4fa0-bbf8-7015acbd9021.png)
# ERD
![Database ER diagram (crow's foot)](https://user-images.githubusercontent.com/7442267/146496462-10315d9a-1863-47c9-ae9e-6bc0337cdbad.png)

# TODO:
General
1. seperate plot and title out to make movie_info a imdb_fact table for better star schema adherence
2. Bashscript to run scraper and move file to cleaner
3. Schedule a cronjob to do this at a regular interval
4. Migrate to AWS
5. Institute a manager like Airflow

Scraper
1. Fix list output
2. Add S3 bucket file dumping
3. More informative logging and dump it to a database

Cleaner
1. Company name extraction handle foreign companies
2. Optimize for speed
3. Institute unit tests, and more rigorous validation
4. More informative logging and dump to a database

# Other Notes:

