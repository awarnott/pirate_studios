-- Q7. Show the difference between the price of a booking and the price of the first booking
--     of that room type. NOTE this SQL relies on a view created in q6.sql.

with first_booking as (select room_type, min(starts_at) first_booking_date
                       from v_bookings_room_type
                      group by room_type),
     first_price as (select min(v_bookings_room_type.price) price,
                            v_bookings_room_type.room_type
                       from v_bookings_room_type,
                            first_booking
                      where starts_at = first_booking.first_booking_date
                        and v_bookings_room_type.room_type = first_booking.room_type
                      group by v_bookings_room_type.room_type)
select v_bookings_room_type.id,
       v_bookings_room_type.room_type,
       v_bookings_room_type.price,
       first_price.price first_price,
       v_bookings_room_type.starts_at,
       v_bookings_room_type.ends_at
  from v_bookings_room_type
  left join first_price on (v_bookings_room_type.room_type = first_price.room_type);

