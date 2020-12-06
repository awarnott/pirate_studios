-- Create all needed tables.
drop table if exists bookings cascade;
drop table if exists rooms    cascade;

create table rooms (id        bigint primary key,
                    room_name text);

create table bookings (id         bigint primary key,
                       room_id    bigint references rooms(id),
                       price      numeric,
                       deleted_at timestamp,
                       starts_at  timestamp with time zone,
                       ends_at    timestamp with time zone);

copy rooms from '/home/adam/tests/Pirate/rooms.csv' csv delimiter ',' header;
copy bookings from '/home/adam/tests/Pirate/bookings.csv' csv delimiter ',' header;

create index booking_room_id on bookings(room_id);

-- Q1 Remove all cancelled bookings

delete from bookings where deleted_at is not null;

-- Q3 Extract room type from room name and put in its own (new) column
--    Note Q2 requires a room type that is not created until Q3 so questions
--    2 and 3 are switched.

alter table rooms drop column if exists room_type;

alter table rooms add column room_type text;

update rooms
   set room_type = trim(substring(room_name, '[^0-9]+'));

-- Q2 Join rooms data to booking data.

drop view if exists v_bookings_room_type cascade;

create view v_bookings_room_type as
  select bookings.id,
         bookings.room_id,
         bookings.price,
         bookings.deleted_at,
         bookings.starts_at,
         bookings.ends_at,
         rooms.room_type
   from bookings left join rooms on (bookings.room_id = rooms.id);

-- Q4 Create a duration of booking column and populate
alter table bookings drop column if exists booking_duration;

alter table bookings
  add column booking_duration numeric;

update bookings
   set booking_duration = (extract(epoch from ends_at) - extract(epoch from starts_at))/3600;

--Q5 Report on the total hours booked, grouped by start date year and room_type

-- First we'll re-create our view of the booking and room type to include the new room_type column

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

-- Not sure about the ordering of the groupings so provided both
-- Grouped by room type within year
select extract(year from starts_at) as year, room_type, sum(booking_duration) as total_hours
  from v_bookings_room_type
 group by rollup (extract(year from starts_at), room_type)
 order by year, room_type;

-- Grouped by year within room type
select room_type, extract(year from starts_at) as year, sum(booking_duration) as total_hours
  from v_bookings_room_type
 group by rollup ( room_type, extract(year from starts_at))
 order by room_type, year;

-- Q6 Same as Q5

-- Q7 Show the difference between the price of a booking and the price of the first booking
--    of that room type

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
  