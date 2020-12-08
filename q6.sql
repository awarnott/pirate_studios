-- Q6. Show a report of booking duration by room type within year.
--     NOTE this report relies on a view with the booking duration value so that is
--     created first. The booking duration column itself was created in q4.py

drop view if exists v_bookings_room_type cascade;

create view v_bookings_room_type as
  select bookings.id,
         bookings.room_id,
         bookings.price,
         bookings.deleted_at,
         bookings.starts_at,
         bookings.ends_at,
         bookings.booking_duration,
         rooms.room_type
   from bookings left join rooms on (bookings.room_id = rooms.id);

-- Booking duration totals grouped by room type within year
select extract(year from starts_at) as year, room_type, sum(booking_duration) as total_hours
  from v_bookings_room_type
 group by rollup (extract(year from starts_at), room_type)
 order by year, room_type;

