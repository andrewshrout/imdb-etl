import pandas as pd
import glob
import re
from sqlalchemy import create_engine
from datetime import date

#PATH
#TODO: Make this dynamic with OS
file_path = glob.glob('./transformations/*.csv.gz')
df = pd.read_csv(file_path[0], compression='gzip')

#Create engine
#engine = create_engine('postgresql://username:password@databasehost:port/databasename')
engine = create_engine('postgresql://postgres:postgres@172.17.0.1:5432/postgres')
conn = psycopg2.connect('postgresql://postgres:postgres@172.17.0.1:5432/postgres')

#FUNCTIONS
def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

def reformatStringToDf(string):
    """
        Until scrapy formating is fixed, this is a stopgap to reconvert the actors/writers/etc into dataframes
        
        TODO: Fix scrapy scraping and remove janky production company cleaning
    """
    #temp = re.findall("'([^']*)'", string) -- breaks on French companies
    temp = string.replace('"', '').replace("'",'').replace('[','').replace(']','').replace('(','')[:-1].strip().split('),')
    storage = []
    for item in temp:
        split = item.rsplit(',', 1)
        storage.append(split[0])
        storage.append(split[1])
    temp = list(pairwise(storage))
    #handle odd none-values from scrape
    for item in temp:
        if item == (' None', ' None'):
            temp.remove(item)
    temp_df = pd.DataFrame(temp, columns=['Name', 'Id'])
    temp_df['Id'] = temp_df['Id'].astype(int)
    return temp_df

def dataFramer(string):
    """
        Takes lists of people in the dataframe and unpacks them into a dataframe for insertion/concatenation
    """
    final_df = pd.DataFrame(columns = ['Name', 'Id'])
    for index, item in enumerate(df[string]):
        temp_df = reformatStringToDf(item)
        final_df = final_df.append(temp_df, ignore_index = True, sort = False)
    final_df = final_df.drop_duplicates()
    return final_df


def personAndId(string):
    """
        Creates a table that matches movieId to person for connecting their fact tables
    """
    final_df = pd.DataFrame(columns = ['Name', 'Id', 'MovieId'])
    for index, item in enumerate(df[string]):
        temp_df = reformatStringToDf(item)
        temp_df['MovieId'] = df['movieId'][index]
        final_df = final_df.append(temp_df, ignore_index = True, sort = False)
    final_df = final_df.drop(['Name'], axis=1).drop_duplicates()
    return final_df

def insertHumanDataFrame(dfName, idName):
    df = personAndId(dfName)
    df = df.rename(columns={"Id": '{}id'.format(idName), 'MovieId': 'movieid'})
    with engine.begin() as connection:
        df.to_sql(dfName, con=connection, if_exists='append', index = False)

def findBaseGenre(df):
    """
        Extracts base genre from URL that the movie was scraped from. This differs from subgenres (which comes from movie data.)
        Removes beginning of url ('https://www.imdb.com/search/title/?genres=')
        Then slices off the end ('&explore=title_type,genres&title_type=movie&ref_=adv_explore_rhs')
    """
    string = df[42:].split("&")[0].upper()
    return string


#DB Functions
#TODO: Test insertions more rigorously with these.
def table_exists(con, table_str):
    exists = False
    try:
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cur.fetchone()[0]
        print(exists)
        cur.close()
    except psycopg2.Error as e:
        print(e)
    return exists

def get_table_col_names(con, table_str):
    col_names = []
    try:
        cur = con.cursor()
        cur.execute("select * from " + table_str + " LIMIT 0")
        for desc in cur.description:
            col_names.append(desc[0])        
        cur.close()
    except psycopg2.Error as e:
        print(e)

    return col_names

#LOGGING
#missingness / data quality
def quick_stats(df):
    """
    Args:
        df: cleaned df
    Returns
        missingness, unique values
    """
    today = date.today()
    with open('log.txt', 'w') as f:
        f.write('log ' + str(today))
        f.write('\nRows:' + str(df.shape[0]))
        f.write('\nMissing values:' + str(df.isnull().values.sum()))
        f.write('\nUnique Values  :\n' + str(df.nunique()))
        #make a list of the variables that contain missing values
        vars_with_na=[var for var in df.columns if df[var].isnull().sum()>1]
        #print the variable name and the percentage of missing values
        for var in vars_with_na:
            f.write('\n' + str(var) + str(np.round(df[var].isnull().mean(),3)) + '% missing values')
    f.closed

    

#TODO: testing
#acceptance tests
#genres have certain values
#ranks are all between 1 and 50
#verify table has any data at all
#verify table doesn't have too many nulls
#test the cleaner with a sample dataset (and that it looks the same at the end)
#test edge cases (foreign names, companies, etc)


def imdb_cleaner(df):
    """
        Input: df from imdb_scraper
        Timing:
        Approach: flatten genres, explode colums with humans / companies, then insert into database after correcting columns
        Improvements:
            -Collect more info on humans (DOB, oscars, etc)
            -Collect box office data
    """
    #initial validation by dropping any rows with all n/a in case scrape went poorly
    df.dropna(how='all', inplace = True)
    #drop all columns with all n/a
    df.dropna(axis=1, how='all')

    #Find base genre, and all subgenres
    df['genres'] = df['genres'].fillna('None')
    #base genre extraction
    df['baseGenre'] = df['url'].apply(findBaseGenre)


    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
    genre_df = pd.DataFrame(columns = genres)

    #match the genres if they are present and use 1 or 0 for future ML
    for index, item in enumerate(df['genres'].fillna(',').str.split(',')):
            matching = [s for s in genres if any(xs in s for xs in item)]
            genre_df = genre_df.append(dict((k, 1) for k in matching), ignore_index=True)

    #join the DF's with their subgenres
    genre_df = df[['movieId']].join(genre_df)
    genre_df = genre_df.rename(columns={"Film-Noire":"filmnoire", "Sci-Fi":"scifi"})
    with engine.begin() as connection:
        genre_df.to_sql('subgenres', con=connection, if_exists='append', index = False)
    #people DF (name, id) for matching in star schema
    #iterate through all people (writers, actors, producers, directors), append to new DF, remove duplicates then insert into SQL
    people_df = pd.DataFrame(columns=['Name', 'Id'])
    peopleGroups = ['writers', 'actors', 'directors', 'producers']

    for group in peopleGroups:
        temp_df = dataFramer(group)
        people_df = people_df.append(temp_df, ignore_index= True, sort= False)
    people_df['Name'] = people_df['Name'].str.upper().str.strip()

    #sanitize that these people are unique then insert
    people_df = people_df.rename(columns={"Name":"name", "Id":"id"}).drop_duplicates()
    with engine.begin() as connection:
        people_df.to_sql('people', con=connection, if_exists='append', index = False)

    #company DF (name, id)
    #TODO: handle edge case companies
    #french companies break regex
    #company_data = dataFramer(df['companies'])
    #company + movieId
    #movie_companies = personAndId('companies')

    #insert actors and their movies
    insertHumanDataFrame('actors', 'actor')

    #insert writers and their movies
    insertHumanDataFrame('writers', 'writer')

    #director + movieId
    insertHumanDataFrame('directors', 'director')

    #producer + movieId
    insertHumanDataFrame('producers', 'producer')

    #movie_info (movieId, title, rank, year, plot, runtime, rating, votes)
    movie_info = df[['movieId', 'title', 'year', 'plot', 'runtime', 'rating', 'votes']].rename(columns={"movieId" : 'movieid'})
    movie_info['title'] = movie_info['title'].str.upper().str.strip()
    with engine.begin() as connection:
        movie_info.to_sql('movie_info', con=connection, if_exists='append', index = False)

    movie_rankings = df[['movieId', 'baseGenre', 'rank']].rename(columns={"movieId":"movieid", "baseGenre": "basegenre"})
    with engine.begin() as connection:
        movie_rankings.to_sql('rankings', con=connection, if_exists='append', index = False)

def main():
    imdb_cleaner(df)
    #TODO: make this more parsable and insert it into database
    quick_stats(df)

if __name__ == "__main__":
    main()