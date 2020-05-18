"""
The following SQL queries are created to support the creation of tables, deletion of tables or inserting of data into tables by create_tables.py or etl.py.
"""

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays ( 
                            songplay_id SERIAL,
                            start_time TIMESTAMP NOT NULL,
                            user_id int NOT NULL,
                            level varchar,
                            song_id varchar,
                            artist_id varchar,
                            session_id int,
                            location varchar,
                            user_agent varchar,
                            PRIMARY KEY (songplay_id),
                            UNIQUE (start_time, user_id, song_id, artist_id));
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                        user_id int,
                        first_name varchar,
                        last_name varchar,
                        gender varchar,
                        level varchar NOT NULL,
                        PRIMARY KEY (user_id));
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
                        song_id varchar,
                        title varchar,
                        artist_id varchar,
                        year int,
                        duration numeric,
                        PRIMARY KEY (song_id));
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                          artist_id varchar,
                          name varchar,
                          location varchar,
                          latitude numeric,
                          longitude numeric,
                          PRIMARY KEY (artist_id));
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                        start_time TIMESTAMP,
                        hour int NOT NULL,
                        day int NOT NULL,
                        week int NOT NULL,
                        month int NOT NULL,
                        year int NOT NULL,
                        weekday varchar NOT NULL,
                        PRIMARY KEY (start_time));
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time,user_id,level,song_id,artist_id,
                            session_id, location,user_agent)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (start_time, user_id, song_id, artist_id) DO UPDATE
                            SET start_time = %s,
                                user_id = %s,
                                level = %s,
                                song_id = %s,
                                artist_id = %s,
                                session_id = %s,
                                location = %s,
                                user_agent = %s;
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET
                        level = EXCLUDED.level;
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
                          VALUES (%s, %s, %s, %s, %s)
                          ON CONFLICT (artist_id) DO UPDATE SET
                          location = EXCLUDED.location,
                          latitude = EXCLUDED.latitude,
                          longitude = EXCLUDED.longitude;
""")


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""SELECT songs.song_id, songs.artist_id
                  FROM songs
                  JOIN artists
                  ON songs.artist_id = artists.artist_id
                  WHERE songs.title = %s
                  AND artists.name = %s
                  AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]