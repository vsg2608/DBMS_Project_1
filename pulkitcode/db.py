import psycopg2 as pg

dbname = "postgres"
passsword =
conn = pg.connect(database = dbname, user = "postgres", password = password, host = "localhost", port = "5432")
cur = conn.cursor()

conn.autocommit = True
#cur.execute("DROP DATABASE project;")
crtdb = """CREATE DATABASE project;"""
cur.execute(crtdb)
conn.commit()
cur.execute(r"\CONNECT project;")
conn.autocommit = False


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

crttbl = "CREATE TABLE rest (Restaurant_ID int,	Restaurant_Name VARCHAR, Address VARCHAR," \
         " Locality VARCHAR, Longitude float, Latitude float, Cuisines VARCHAR, AverageCost_for_two float, " \
         "Currency VARCHAR, Has_Table_booking BOOL,	Has_Online_delivery BOOL, Price_range FLOAT," \
         " Aggregate_rating FLOAT, Votes INT) ;"
cur.execute(crttbl)

crttbl = "CREATE TABLE ratings (Aggregate_rating FLOAT, Rating_color VARCHAR, Rating_text VARCHAR);"
cur.execute(crttbl)

crttbl = "CREATE TABLE city (Locality VARCHAR, City VARCHAR, Country_Code INT);"
cur.execute(crttbl)

crttbl = "CREATE TABLE country (Country_Code INT, Country VARCHAR);"
cur.execute(crttbl)

crttbl = "CREATE TABLE cuisine (Cuisine VARCHAR, Cuisine_Code INT);"
cur.execute(crttbl)

crttbl = "CREATE TABLE Rest_Cuisine (Rest_ID INT, Cuisine_Code INT);"
cur.execute(crttbl)

crttbl = "CREATE TABLE users (User_ID INT, Password VARCHAR, Name VARCHAR, DoB DATE, " \
         "Gender CHAR CHECK (Gender IN ('M','F')), Address VARCHAR, Locality VARCHAR);"
cur.execute(crttbl)

crttbl = "CREATE TABLE Transaction (Id INT, UserId INT, RestId INT, BookedOn TIMESTAMP, BookedFor TIMESTAMP," \
         " No_People INT, Rating INT CHECK (BookedFor - BookedOn < '1 day'::interval)," \
         " CHECK (BookedFor > BookedOn));"
cur.execute(crttbl)

conn.commit()

#cur.execute("\\COPY country FROM 'C:\\Users\\Admin\\Desktop\\Pulkit\\Sem 8\\COL362\\Project\\Country-Code.csv';")
'''
with open('Country-Code.csv', 'r') as f:
    next(f)  # Skip the header row.
    #cur.copy_from(f, 'temp', sep =',')
    cur.copy_expert("copy temp from stdin (format csv)", f)
'''
with open('dict.csv', 'r') as f:
    next(f)  # Skip the header row.
    cur.copy_expert("copy cuisine from stdin (format csv)", f)

with open('restid_cuisineid.csv', 'r') as f:
    next(f)  # Skip the header row.
    cur.copy_expert("copy Rest_Cuisine from stdin (format csv)", f)

putdata = "INSERT INTO rest (Restaurant_ID, Restaurant_Name, Address," \
         " Locality, Longitude, Latitude, Cuisines, AverageCost_for_two, " \
         "Currency, Has_Table_booking,	Has_Online_delivery, Price_range, Aggregate_rating, Votes) " \
         "SELECT Restaurant_ID, Restaurant_Name, Address," \
         " Locality, Longitude, Latitude, Cuisines, AverageCost_for_two, " \
         "Currency, Has_Table_booking,	Has_Online_delivery, Price_range, Aggregate_rating, Votes FROM temp;"
cur.execute(putdata)
conn.commit()

putdata = "INSERT INTO city SELECT Locality, City, Country_Code FROM temp;"
cur.execute(putdata)

putdata = "INSERT INTO ratings SELECT Aggregate_rating, Rating_color, Rating_text FROM temp;"
cur.execute(putdata)

conn.commit()
#cur.execute("SELECT count(*) FROM temp")
#conn.commit()

conn.close()
