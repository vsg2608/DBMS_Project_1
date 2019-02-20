-- select a.rest_id from rest_cuisine as a, rest_cuisine as b where a.cuisine_code = 52 and b.cuisine_code = 70 and a.rest_id = b.rest_id;

-- Search By City
drop table if exists tempcity;
select rest.restaurant_name into temp tempcity from rest, city where rest.localityid = city.id and lower(city.city) = lower('agra');

-- select rest.restaurant_name from rest, city where rest.localityid = city.id and lower(city.city) = lower('cityname');

-- Filter by locality
-- select 
