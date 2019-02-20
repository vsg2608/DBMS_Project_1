import psycopg2 as pg

dbname = "project"
password = "Password@123"
conn = pg.connect(database = dbname, user = "postgres", password = password, host = "13.233.41.140", port = "5432")
cur = conn.cursor()

"""
conn.autocommit = True
#cur.execute("DROP DATABASE project;")
crtdb = "CREATE DATABASE project;"
cur.execute(crtdb)
conn.commit()
cur.execute("\CONNECT project;")
conn.autocommit = False
"""

cur.execute("DROP TABLE IF EXISTS city, country, cuisine, ratings, rest, rest_cuisine, temp, transaction, users;")

crttbl = "CREATE TABLE temp (Restaurant_ID int,	Restaurant_Name VARCHAR, Country_Code int, City VARCHAR, Address VARCHAR," \
         " Locality VARCHAR, Locality_Verbose VARCHAR,Longitude float, Latitude float, Cuisines VARCHAR, " \
         "AverageCost_for_two float, Currency VARCHAR, Has_Table_booking BOOL,	Has_Online_delivery BOOL, " \
         "Is_delivering_now BOOL, Switch_to_order_menu BOOL, Price_range FLOAT," \
         " Aggregate_rating FLOAT, Rating_color VARCHAR, Rating_text VARCHAR, Votes INT) ;"

cur.execute(crttbl)
conn.commit()


#cur.execute(\\COPY temp FROM 'C:\\Users\\Admin\\Desktop\\Pulkit\\Sem 8\\COL362\\Project\\zomato3.csv' DELIMITERS ',' CSV HEADER;)
with open('zomato3.csv', 'r') as f:
    next(f)  # Skip the header row.
    #cur.copy_from(f, 'temp', sep =',')
    cur.copy_expert("copy temp from stdin (format csv)", f)
conn.commit()

crttbl = "CREATE TABLE ratings (Aggregate_rating FLOAT PRIMARY KEY, Rating_color VARCHAR, Rating_text VARCHAR);"
cur.execute(crttbl)

crttbl = "CREATE TABLE city (ID SERIAL PRIMARY KEY, Locality VARCHAR, City VARCHAR, Country_Code INT);"
cur.execute(crttbl)

crttbl = "CREATE TABLE country (Country_Code INT PRIMARY KEY, Country VARCHAR);"
cur.execute(crttbl)

crttbl = "CREATE TABLE cuisine (Cuisine VARCHAR, Cuisine_Code INT);"
cur.execute(crttbl)

crttbl = "CREATE TABLE rest (Restaurant_ID INT PRIMARY KEY, Restaurant_Name VARCHAR," \
         " Address VARCHAR, LocalityID INT REFERENCES city(ID), Longitude float, Latitude float, " \
         "Cuisines VARCHAR, AverageCost_for_two float, " \
         "Currency VARCHAR, Has_Table_booking BOOL,	Has_Online_delivery BOOL, Price_range FLOAT," \
         " Aggregate_rating FLOAT REFERENCES ratings(Aggregate_rating), Votes INT) ;"
cur.execute(crttbl)

crttbl = "CREATE TABLE Rest_Cuisine (Rest_ID INT REFERENCES rest (Restaurant_ID), Cuisine_Code INT);"
cur.execute(crttbl)

crttbl = "CREATE TABLE users (User_ID INT PRIMARY KEY, Password VARCHAR, Name VARCHAR, email text not null unique,"\
          "DoB DATE, Gender CHAR CHECK (Gender IN ('M','F')), Address VARCHAR, Locality VARCHAR);"
cur.execute(crttbl)

crttbl = "CREATE TABLE Transaction (Id INT, UserId INT REFERENCES users(User_ID)," \
         " RestId INT REFERENCES rest(Restaurant_ID), BookedOn TIMESTAMP, BookedFor TIMESTAMP," \
         " No_People INT, Rating INT CHECK (BookedFor - BookedOn < '1 day'::interval)," \
         " CHECK (BookedFor > BookedOn));"
cur.execute(crttbl)

conn.commit()

#cur.execute("\\COPY country FROM 'C:\\Users\\Admin\\Desktop\\Pulkit\\Sem 8\\COL362\\Project\\Country-Code.csv';")

putdata = "INSERT INTO city (Locality, City, Country_Code) SELECT DISTINCT Locality, City, Country_Code" \
          " FROM temp ORDER BY Country_Code, City, Locality;"
cur.execute(putdata)

putdata = "INSERT INTO ratings SELECT DISTINCT Aggregate_rating, Rating_color, Rating_text FROM temp;"
cur.execute(putdata)

putdata = "INSERT INTO rest (Restaurant_ID, Restaurant_Name, Address," \
         " LocalityID, Longitude, Latitude, Cuisines, AverageCost_for_two, " \
         "Currency, Has_Table_booking,	Has_Online_delivery, Price_range, Aggregate_rating, Votes) " \
         "SELECT Restaurant_ID, Restaurant_Name, Address," \
         " city.ID, Longitude, Latitude, Cuisines, AverageCost_for_two, " \
         "Currency, Has_Table_booking,	Has_Online_delivery, Price_range, Aggregate_rating, Votes FROM temp, city" \
         " WHERE temp.Locality = city.Locality AND temp.city = city.city AND temp.Country_Code = city.Country_Code;"
cur.execute(putdata)


with open('Country-Code.csv', 'r') as f:
    next(f)  # Skip the header row.
    #cur.copy_from(f, 'temp', sep =',')
    cur.copy_expert("copy country from stdin (format csv)", f)

with open('dict.csv', 'r') as f:
    cur.copy_expert("copy cuisine from stdin (format csv)", f)

with open('restid_cuisineid.csv', 'r') as f:
    cur.copy_expert("copy Rest_Cuisine from stdin (format csv)", f)
#conn.commit()

conn.commit()
#cur.execute("SELECT count(*) FROM temp")
#conn.commit()

conn.close()
