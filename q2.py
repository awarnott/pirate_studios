# Q2. This code will create a view that joins the bookings and rooms data

import psycopg2
import sys

def get_connection():
  conn = psycopg2.connect("dbname=postgres user=postgres host=localhost port=5432")
  cur = conn.cursor()
  return conn, cur

def join_bookings_rooms(cur):
    print('Creating a view of rooms data and bookings data joined by id of rooms')
    cur.execute('drop view if exists v_bookings_room_type cascade')
    sql_txt = 'create view v_bookings_room_type as '   \
                      'select bookings.id booking_id,' \
                             'bookings.room_id,'       \
                             'bookings.price,'         \
                             'bookings.deleted_at,'    \
                             'bookings.starts_at,'     \
                             'bookings.ends_at,'       \
                             'rooms.room_type,'        \
                             'rooms.room_name '        \
                        'from bookings left join rooms on (bookings.room_id = rooms.id)'

    cur.execute(sql_txt)
    
def main():
  try:
    print('Joining rooms data to bookings data')
    conn, cur = get_connection()
    join_bookings_rooms(cur)
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
