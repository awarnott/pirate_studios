# Q3. This code will extract the room type from room_name column and put it in a new column

import psycopg2
import sys

def get_connection():
  conn = psycopg2.connect("dbname=postgres user=postgres host=localhost port=5432")
  cur = conn.cursor()
  return conn, cur

def extract_room_type(cur):
    print('Altering rooms table. Adding a new column: room_type')
    cur.execute('alter table rooms drop column if exists room_type cascade')
    cur.execute('alter table rooms add column room_type text')
    
    print('Populating room_type column')
    cur.execute('update rooms set room_type = trim(substring(room_name, %s))', ('[^0-9]+',))

def main():
  try:
    print('Extracting room type from room_name and storing in a new column')
    conn, cur = get_connection()
    extract_room_type(cur)
    conn.commit()

  except (Exception, psycopg2.Error) as e:
    if 'conn' in locals():
      conn.rollback()
    print('Failure: all changes have been rolled back')
    print(e)
    print sys.exc_info()[0]

  else:
    print('Success: all changes committed')
    
  finally:
    if 'cur' in locals():
      cur.close
    if 'conn' in locals():
      conn.close

if __name__ == '__main__':
  main()
