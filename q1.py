# Q1. This code will remove all cancelled bookings from the bookings table

import psycopg2
import sys

def get_connection():
  conn = psycopg2.connect("dbname=postgres user=postgres host=localhost port=5432")
  cur = conn.cursor()
  return conn, cur

def delete_cancelled(cur):
    cur.execute('delete from bookings where deleted_at is not null')
    print('Removing {} cancelled bookings'.format(cur.rowcount))

def main():
  try:
    print('Attempting to remove all cancelled bookings from bookings table')
    conn, cur = get_connection()
    delete_cancelled(cur)
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
