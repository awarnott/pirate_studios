# pirate_studios
Hiring test

The answers are contained in q1.py - q5.py, and q6.sql and q7.sql. The code uses the pyscopg2 library to access a Postgres database so the connection parameters will have to be changed to match your setup.
For question 2, I wasn't quite sure what was meant by 'join the booking data and the room data'. In the context of a database and SQL, I took this to mean a VIEW. I used a LEFT JOIN of the bookings table to the rooms table in case there was ever an instance where there was a booking without a room, the booking would still show in the output.
The view created in question 3 was needed by question 2 so first run q3.py and then q2.py.
For question 5, I wasn't sure of the grouping order so I chose room types within years.

The first 6 SQL statements in test.sql can be used to create the db tables and load the data if needed. The path to the data files will have to be updated to match your setup.

Thanks Adam
