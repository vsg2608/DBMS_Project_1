-- select a.rest_id from rest_cuisine as a, rest_cuisine as b where a.cuisine_code = 52 and b.cuisine_code = 70 and a.rest_id = b.rest_id;

-- Search By City, enter city name in the space provided, change the output columns as necessary
drop table if exists tempcity;
select restaurant_id, restaurant_name into temp tempcity from rest, city where rest.localityid = city.id and lower(city.city) = lower('agra');

-- select rest.restaurant_name from rest, city where rest.localityid = city.id and lower(city.city) = lower('cityname');

-- create filter table
select rest.* into temp filterresult from rest, tempcity where rest.restaurant_id = tempcity.restaurant_id;

-- Filter by locality, input name of locality preferably give options after few letters
delete from filterresult where filterresult.restaurant_id not in (select restaurant_id from filterresult, city where filterresult.localityid = city.id and lower(city.locality) = lower(''));

-- Filter by rating, input/choose from options rating above which (included) to be selected
delete from filterresult where filterresult.restaurant_id not in (select restaurant_id from filterresult where filterresult.aggregate_rating >= input);
