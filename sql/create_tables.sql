--Creation of movie_info table
CREATE TABLE IF NOT EXISTS movie_info (
    movieid INT UNIQUE NOT NULL,
    title VARCHAR(250) NOT NULL,
    year INT,
    plot TEXT,
    runtime FLOAT,
    rating FLOAT,
    votes INT,
    PRIMARY KEY (movieId)
    );

--Creation of rankings table
CREATE TABLE IF NOT EXISTS rankings (
    movieid INT NOT NULL,
    basegenre VARCHAR(250) NOT NULL,
    rank INT NOT NULL
)

--Creation of people table
CREATE TABLE IF NOT EXISTS people (
    id INT UNIQUE NOT NULL,
    name VARCHAR(250) NOT NULL
);

--Creation of actors table for cast
CREATE TABLE IF NOT EXISTS actors (
    actorid INT NOT NULL,
    movieid INT NOT NULL
);

--Creation of writers table
CREATE TABLE IF NOT EXISTS writers (
    writerid INT NOT NULL,
    movieid INT NOT NULL
);
--Creation of producers table
CREATE TABLE IF NOT EXISTS producers (
    producerId INT NOT NULL,
    movieId INT NOT NULL
);

--Creation of directors table
CREATE TABLE IF NOT EXISTS directors (
    directorId INT NOT NULL,
    movieId INT NOT NULL
);

--Creation of subgenre table
CREATE TABLE IF NOT EXISTS subgenres (
    movieId INT UNIQUE NOT NULL,
    action INT,
    adventure INT,
    animation INT,
    biography INT,
    comedy INT,
    crime INT,
    documentary INT,
    drama INT,
    family INT,
    fantasy INT,
    filmnoire INT,
    history INT,
    horror INT,
    music INT,
    musical INT,
    mystery INT,
    romance INT,
    scifi INT,
    sport INT,
    thriller INT,
    war INT,
    western INT,
    CONSTRAINT fk_movie_info_exists
            FOREIGN KEY(movieId)
        REFERENCES movie_info(movieId)
);