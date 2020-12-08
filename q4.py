# Q4. Create a new column in bookings for the duration of the booking

import psycopg2
import sys

def get_connection():
  conn = psycopg2.connect("dbname=postgres user=postgres host=localhost port=5432")
  cur = conn.cursor()
  return conn, cur

def create_durations(cur):
    print('Altering bookings table. Adding a new column: duration')
    cur.execute('alter table bookings drop column if exists booking_duration cascade')
    cur.execute('alter table bookings add column booking_duration numeric')
    
    print('Populating duration column')
    cur.execute('update bookings set booking_duration = (extract(epoch from ends_at) - extract(epoch from starts_at))/3600')

def main():
  try:
    print('Calculating booking duration and storing it in a new column')
    conn, cur = get_connection()
    create_durations(cur)
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
