# Q5. Create a report of total hours booked, grouped by year of booking start date and room type

import psycopg2
import sys

def get_connection():
  conn = psycopg2.connect("dbname=postgres user=postgres host=localhost port=5432")
  cur = conn.cursor()
  return conn, cur

def create_view(cur):
  print('Re-create the bookings_room_type view. Adding in the duration column')
  cur.execute('drop view if exists v_bookings_room_type cascade')
  cur.execute('create view v_bookings_room_type '         \
                  'as select bookings.id,'                \
                            'bookings.room_id,'           \
                            'bookings.price,'             \
                            'bookings.deleted_at,'        \
                            'bookings.starts_at,'         \
                            'bookings.ends_at,'           \
                            'bookings.booking_duration,'  \
                            'rooms.room_type '            \
                            'from bookings left join rooms on (bookings.room_id = rooms.id)')

def create_report(cur):
  print('Sum booking hours by start date year and room type')
  sql_txt = 'select extract(year from starts_at) as year,'    \
                   'room_type,'                               \
                   'sum(booking_duration) as total_hours '    \
                   'from v_bookings_room_type '               \
                   'group by rollup (extract(year from starts_at), room_type)' \
             'order by year, room_type'

  cur.execute(sql_txt)
  report_rows = cur.fetchall()

  return report_rows

def print_report(report_rows):
  print('')
  print('Total Hours Booked by Room Type within Year')
  print('')
  print(' Year    Room Type      Hours')
  print(' ----  --------------  -------')
  for row in report_rows:
    if isinstance(row[0], type(None)): # unfortunately each cell of the output can have its own type
      year_txt = ''
    else:
      year_txt = str(row[0])[:4]
    print("%5s  %14s  %7d" %(year_txt, str(row[1] or ''), row[2]))
  print('')

def main():
  try:
    print('Creating booking rollup report')
    conn, cur = get_connection()
    create_view(cur)
    conn.commit()
    print('Success: all changes committed')
    report_rows = create_report(cur)
    print_report(report_rows)

  except (Exception, psycopg2.Error) as e:
    if 'conn' in locals():
      conn.rollback()
    print('Failure: all changes have been rolled back')
    print(e)
    print sys.exc_info()[0]

  finally:
    if 'cur' in locals():
      cur.close
    if 'conn' in locals():
      conn.close

if __name__ == '__main__':
  main()
