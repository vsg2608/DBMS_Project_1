-- -- select a.rest_id from rest_cuisine as a, rest_cuisine as b where a.cuisine_code = 52 and b.cuisine_code = 70 and a.rest_id = b.rest_id;

-- -- Search By City, enter city name in the space provided, change the output columns as necessary
-- drop table if exists tempcity;
-- select restaurant_id, restaurant_name into temp tempcity from rest, city where rest.localityid = city.id and lower(city.city) = lower('agra');

-- -- select rest.restaurant_name from rest, city where rest.localityid = city.id and lower(city.city) = lower('cityname');

-- -- create filter table, create everytime a new city is used or filters are changed (not added)
-- select rest.* into temp filterresult from rest, tempcity where rest.restaurant_id = tempcity.restaurant_id;

-- -- Filter by name, substring possible
-- delete from filterresult where filterresult.restaurant_id not in (select restaurant_id from filterresult where lower(filterresult.restaurant_name) LIKE lower('%%'));

-- -- Filter by locality, input name of locality preferably give options after few letters
-- delete from filterresult where filterresult.restaurant_id not in (select restaurant_id from filterresult, city where filterresult.localityid = city.id and lower(city.locality) = lower(''));

-- -- Filter by rating, input/choose from options rating above which (included) to be selected
-- delete from filterresult where filterresult.restaurant_id not in (select restaurant_id from filterresult where filterresult.aggregate_rating >= input);

-- -- Filter by votes, input/choose from options rating above which (included) to be selected
-- delete from filterresult where filterresult.restaurant_id not in (select restaurant_id from filterresult where filterresult.votes >= input);

-- -- Filter by average cost (for a currency), input cost as well as currency, search valid only if the restaurant sells in that currency
-- -- edit: filter by cost range (column with values 1,2,3,4)
-- delete from filterresult where filterresult.restaurant_id not in (select restaurant_id from filterresult where filterresult.price_range >= input);

-- -- Filter by cuisine AND clause (all cuisine present)
-- loop through input cuisines
-- delete from filterresult where filterresult.restaurant_id not in (select rest_id from rest_cuisine, cuisine where cuisine.cuisine_code = rest_cuisine.cuisine_code AND cuisine.cuisine = '');

-- -- Filter by cuisine OR clause (any cuisine present)
-- delete from filterresult where filterresult.restaurant_id not in (select rest_id from rest_cuisine, cuisine where cuisine.cuisine_code = rest_cuisine.cuisine_code AND cuisine.cuisine IN (''));


-- -- Filter by area around locality (using lat long) (advanced)
-- -- Inserting New User Information
-- -- Insert Into Users (Password, Name, email, dob, gender, address, locality) value ('','','','','','','');

-- -- Insert Into Transaction(userid, restid, bookedon, bookedfor, no_people, rating) value ('','','','','','');
-- -- -- 

-- -- CREATE TRIGGER trig_updateorders
-- -- AFTER INSERT OF rating ON Transaction
-- -- EXECUTE PROCEDURE update_orders();

CREATE FUNCTION update_ratings() RETURNS trigger as
$update_ratings$
DECLARE
    temprate FLOAT;
	tempvote INT;
BEGIN
    select aggregate_rating, votes into temprate, tempvote from rest where rest.restaurant_id = new.restid;
    UPDATE rest SET aggregate_rating = ROUND((((temprate*tempvote)+new.rating)/(tempvote+1))::numeric,1) where rest.restaurant_id = new.restid;
    UPDATE rest SET votes = votes+1 where rest.restaurant_id = new.restid;
    RETURN NULL;
END;
$update_ratings$
language plpgsql;

CREATE TRIGGER trig_updateratings AFTER UPDATE of rating on Transaction FOR EACH ROW EXECUTE PROCEDURE update_ratings();

-- CREATE FUNCTION update_ratings() RETURNS trigger as $update_ratings$ DECLARE temprate FLOAT := select aggregate_rating from rest where rest.restaurant_id = new.restid;BEGIN
--     -- temprate = rest.aggregate_rating;

--     UPDATE rest SET aggregate_rating = ROUND((((temprate*votes)+new.rating)/(temprate+1)),1) where rest.restaurant_id = new.restid;
--     UPDATE rest SET votes = votes+1 where rest.restaurant_id = new.restid;
--     RETURN NULL;
-- END;
-- $update_ratings()$ language plpgsql;
-- CREATE FUNCTION update_orders() RETURNS trigger as $update_orders$
-- BEGIN
    
--     RETURN NULL;
-- END;
-- $update_orders()$ language plpgsql;


