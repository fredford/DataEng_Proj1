# Project: Data Modeling with Postgres

Fraser Redford

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This project creates a Postgres database with tables designed to optimize queries on song play analysis. The objective being to create a database schema and ETL pipeline for analysis.

## Project Datasets

The current data collection is contained in JSON files organized into 'Song Data' and 'Log Data'. The data in each file type is formatted as:

### Song Data Example

```JSON
{
  "num_songs": 1,
  "artist_id": "ARGSJW91187B9B1D6B",
  "artist_latitude": 35.21962,
  "artist_longitude": -80.01955,
  "artist_location": "North Carolina",
  "artist_name": "JennyAnyKind",
  "song_id": "SOQHXMF12AB0182363",
  "title": "Young Boy Blues",
  "duration": 218.77506,
  "year": 0
}
```

### Log Data Example

```JSON
{
  "artist": "Survivor",
  "auth": "Logged In",
  "firstName": "Jayden",
  "gender": "M",
  "itemInSession": 0,
  "lastName": "Fox",
  "length": 245.36771,
  "level": "free",
  "location": "New Orleans-Metairie, LA",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1541033612796,
  "sessionId": 100,
  "song": "Eye Of The Tiger",
  "status": 200,
  "ts": 1541110994796,
  "userAgent": "\"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\"",
  "userId": "101"
}
```

## Schema for Song Play Analysis

Using the song and log datasets the following star schema was generated:

### Fact Table

1. __songplays__ - Record in log data associated with song plays
   - *songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

### Dimension Tables

1. __users__ - Users of the app
    - *user_id, first_name, last_name, gender, level*
2. __songs__ - Songs in the music library
    - *song_id, title, artist_id, year, duration*
3. __artists__ - Artists in the music library
    - *artist_id, name, location, latitude, longitude*
4. __time__ - Timestamps of records in songplays broken down into specific units
    - *start_time, hour, day, week, month, year, weekday*

## Program Layout

`sql_queries.py` contains all of the SQL queries that will be executed including creating the tables, dropping tables, inserting data into the tables, and selecting songs played.

`create_tables.py` runs the python initialization of the database to execute the SQL queries into the database that is created. The database is created with the host as `127.0.0.1`, the database name as `sparkifydb`, the username as `student` and the password as `student`.

`etl.py` executes the ETL pipeline to load the songs and user data into the Postgres database, by processing each song file into the proper columns for each song and artist. Then processing each log file into the time table, users table and songplays table.

`test.ipynb` runs a test execution of the database by using the sample dataset provided. The Jupyter notebook must be executed after running `create_tables.py` in order to generate the tables and columns needed. The data can be verified for accuracy after running `etl.py` as shown below.

## Dependencies

- Python 3
- pipenv
- PostgreSQL

To install the project dependencies run:
```
pipenv install
```

## Run

To run the project use `pipenv` to activate the environment:
```
pipenv shell
```
Then create the database tables using:
```
./create_tables.py
```
Then execute the ETL by running:
```
./etl.py
```
After performing the provided steps the data can be verified for accuracy by running the `test.ipynb` Jupyter notebook.

