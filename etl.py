import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

import json


def process_song_file(cur, filepath):
    """Function used to process song json files and separate it into song data and artist data.
    
    Arguments:
        cur      -- Cursor object used to connect to PostgreSQL
        filepath -- String holding the file name/pathway to be opened 
    """
    # open song file into dictionary
    file_dict = json.load(open(filepath, 'r'))

    # insert song record
    song_data = (file_dict['song_id'], file_dict['title'], file_dict['artist_id'], file_dict['year'], file_dict['duration'])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = (file_dict['artist_id'],file_dict['artist_name'],file_dict['artist_location'], file_dict['artist_latitude'],file_dict['artist_longitude'])
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    """Function used to process log json files and separate it into time, user, and songplay data.
    
    Arguments:
        cur      -- Cursor object used to connect to PostgreSQL
        filepath -- String holding the file name/pathway to be opened 
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True, convert_dates=['ts'])

    # filter by NextSong action
    df = df[df['page'] == 'NextSong'] 

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit = 'ms') 
    
    # insert time data records
    time_data = [[x, x.hour, x.day, x.week, x.month, x.year, x.dayofweek] for x in t]
    column_labels = ['start_time', 'hour','day','week','month','year','weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.filter(['userId','firstName','lastName','gender','level']).drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        
        cur.execute(songplay_table_insert, songplay_data+songplay_data)


def process_data(cur, conn, filepath, func):
    """Function used to acquire the file paths in the given directory, and perform the specifief function on the information in that directory.
    
    Arguments:
        cur      -- Cursor object used to connect to PostgreSQL
        conn     -- PostgreSQL server connection
        filepath -- Directory to be read and processed
        func     -- The processing function to be used
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()