import mysql.connector 
from mysql.connector import errorcode

conn = mysql.connector.connect(user="root", passwd="kaan")
cursor = conn.cursor()

DB_NAME = 'airline_company'

try:
    cursor.execute("CREATE DATABASE if not exists airline_company")
except mysql.connector.Error as err:
    print('Failed creating database: {}'.format(err))
    exit(1)

try:
    conn.database = DB_NAME
except mysql.connector.Error as err:
    if (err.errno == errorcode.ER_BAD_DB_ERROR):
        create_database(cursor)
        conn.database = DB_NAME
    else:
        print(err)
        exit(1)

# Drop tables
cursor.execute("DROP TABLE IF EXISTS promotion_deadline, flight_arrival")
cursor.execute("DROP TABLE IF EXISTS flight_att, ticket, plane_model")
cursor.execute("DROP TABLE IF EXISTS pass_history, pers_history, flight_pilot")
cursor.execute("DROP TABLE IF EXISTS reservation, seat, menu_option, flight, plane")
cursor.execute("DROP TABLE IF EXISTS store_promotion, food_promotion, flight_promotion")
cursor.execute("DROP TABLE IF EXISTS ticket_staff, store_staff, promotion")
cursor.execute("DROP TABLE IF EXISTS flight_attendant, pilot, flight_personnel")
cursor.execute("DROP TABLE IF EXISTS store, airport, passenger, staff")
cursor.execute("DROP TABLE IF EXISTS person_phone, person_email, person, city")

# Create tables
tables = []
tables.append(
    "CREATE TABLE person( "
    "person_id int PRIMARY KEY AUTO_INCREMENT, "
    "password varchar(40) NOT NULL, "
    "person_name varchar(40) NOT NULL, "
    "address_no int NOT NULL, "
    "street varchar(40) NOT NULL, "
    "town varchar(40) NOT NULL"
    ") ENGINE=InnoDB")

tables.append(
    "CREATE TABLE person_phone( "
    "person_id int, "
    "phone varchar(20), "
    "PRIMARY KEY(person_id, phone), "
    "FOREIGN KEY(person_id) references person(person_id) "
    "ON DELETE CASCADE) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE person_email( "
    "person_id int, "
    "email varchar(40), "
    "PRIMARY KEY(person_id, email), "
    "FOREIGN KEY(person_id) references person(person_id) "
    "ON DELETE CASCADE) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE city( "
    "city_name varchar(40), "
    "country varchar(40), "
    "latitude numeric(8,5) NOT NULL, "
    "longitude numeric(8,5) NOT NULL, "
    "PRIMARY KEY(city_name, country), "
    "check(latitude >= 0 and latitude < 360 and "
    "longitude >= 0 and longitude < 180)) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE airport( "
    "airport_name varchar(40), "
    "city_name varchar(40), "
    "country varchar(40),"
    "PRIMARY KEY(airport_name, city_name, country),"
    "FOREIGN KEY (city_name, country) references city(city_name, country) "
    "on delete cascade) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE store("
    "store_id int PRIMARY KEY AUTO_INCREMENT,"
    "store_name varchar(40) NOT NULL,"
    "owner varchar(40),"
    "airport_name varchar(40),"
    "city_name varchar(40),"
    "country varchar(40),"
    "FOREIGN KEY (airport_name, city_name, country) references "
    "airport(airport_name, city_name, country) "
    "on delete cascade) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE passenger ("
    "pass_id int PRIMARY KEY,"
    "expenditure numeric(4,2) NOT NULL,"
    "prom_expenditure numeric(4,2) NOT NULL,"
    "FOREIGN KEY(pass_id) references person(person_id) "
    "on delete cascade) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE staff ("
    "staff_id int PRIMARY KEY,"
    "salary numeric(12,2) NOT NULL,"
    "FOREIGN KEY(staff_id) references person(person_id) "
    "on delete cascade) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE flight_personnel ("
    "flight_pers_id int PRIMARY KEY,"
    "experience int NOT NULL,"
    "FOREIGN KEY(flight_pers_id) references staff(staff_id) "
    "on delete cascade) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE pilot ("
    "pilot_id int PRIMARY KEY,"
    "rank int NOT NULL,"
    "certificate_type enum('sport', 'recreational', 'private', 'commercial',"
    "'instructor', 'airline transport') NOT NULL,"
    "FOREIGN KEY(pilot_id) references flight_personnel(flight_pers_id) "
    "on delete cascade) ENGINE=InnoDB")

tables.append(
    "CREATE TABLE flight_attendant ("
    "att_id int PRIMARY KEY,"
    "duty varchar(40) NOT NULL,"
    "FOREIGN KEY(att_id) references flight_personnel(flight_pers_id) "
    "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE ticket_staff ("
		"ticket_staff_id int PRIMARY KEY,"
		"ticket_count int NOT NULL,"
		"FOREIGN KEY(ticket_staff_id) references staff(staff_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE store_staff ("
		"store_staff_id int PRIMARY KEY,"
		"sale_count int NOT NULL,"
		"store_id int NOT NULL,"
		"FOREIGN KEY(store_staff_id) references staff(staff_id) "
                "on delete cascade,"
		"FOREIGN KEY(store_id) references store(store_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE promotion ("
		"pass_id int,"
		"prom_id int,"
		"amount int NOT NULL,"
		"PRIMARY KEY(pass_id, prom_id),"
                "UNIQUE KEY(amount),"
		"FOREIGN KEY(pass_id) references passenger(pass_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE store_promotion ("
		"pass_id int,"
		"prom_id int,"
		"product_type enum('alcohol', 'normal') NOT NULL,"
		"PRIMARY KEY(pass_id, prom_id),"
		"FOREIGN KEY(pass_id, prom_id) references promotion(pass_id, prom_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE food_promotion ("
		"pass_id int,"
		"prom_id int,"
		"food_type enum('meal', 'drink') NOT NULL,"
		"PRIMARY KEY(pass_id, prom_id),"
		"FOREIGN KEY(pass_id, prom_id) references promotion(pass_id, prom_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE flight_promotion ("
		"pass_id int,"
		"prom_id int,"
		"domestic binary NOT NULL,"
		"PRIMARY KEY(pass_id, prom_id),"
		"FOREIGN KEY(pass_id, prom_id) references promotion(pass_id, prom_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
                "CREATE TABLE promotion_deadline("
		"amount int,"
		"deadline date,"
		"PRIMARY KEY(amount, deadline),"
		"FOREIGN KEY(amount) references promotion(amount) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE plane("
		"plane_id int PRIMARY KEY AUTO_INCREMENT,"
		"model varchar(20) NOT NULL,"
                "UNIQUE KEY(model)) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE plane_model("
                "model varchar(20) PRIMARY KEY,"
		"capacity int,"
                "plane_range numeric(5,2),"
                "altitude numeric(5,2),"
                "FOREIGN KEY(model) references plane(model) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE flight ("
		"flight_id int PRIMARY KEY AUTO_INCREMENT,"
		"date DATETIME NOT NULL,"
		"plane_id int,"
		"dep_airport_name varchar(40),"
		"dep_city_name varchar(40),"
		"dep_country varchar(40),"
		"arr_airport_name varchar(40),"
		"arr_city_name varchar(40),"
		"arr_country varchar(40),"
		"duration numeric(3,2),"
                "econ_price numeric(6,2),"
		"business_price numeric(6,2),"
		"landed binary NOT NULL,"
		"FOREIGN KEY(plane_id) references plane(plane_id) "
                "on delete cascade,"
		"FOREIGN KEY(dep_airport_name, dep_city_name, dep_country) references "
		"airport(airport_name, city_name, country) "
                "on delete cascade,"
		"FOREIGN KEY(arr_airport_name, arr_city_name, arr_country) references "
		"airport(airport_name, city_name, country) "
                "on delete cascade,"
                "UNIQUE KEY(date, duration)) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE flight_arrival ("
		"date DATETIME,"
		"duration numeric(3,2),"
		"arrival DATETIME,"
		"PRIMARY KEY(date, duration, arrival),"
		"FOREIGN KEY(date, duration) references flight(date, duration) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE seat ("
		"flight_id int,"
		"no int,"
		"class enum('econ', 'business') NOT NULL,"
		"PRIMARY KEY (flight_id, no),"
		"FOREIGN KEY (flight_id) references flight(flight_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE menu_option("
		"flight_id int,"
		"option_id int,"
		"option_name varchar(40) NOT NULL,"
		"PRIMARY KEY (flight_id, option_id),"
		"FOREIGN KEY (flight_id) references flight(flight_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE reservation("
		"flight_id int,"
		"pass_id int,"
		"deadline date NOT NULL,"
		"seat_no int,"
		"PRIMARY KEY(flight_id, pass_id, seat_no),"
		"FOREIGN KEY(pass_id) references passenger(pass_id) "
                "on delete cascade,"
		"FOREIGN KEY(flight_id, seat_no) references seat(flight_id, no) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE pass_history ("
		"flight_id int,"
		"pass_id int,"
		"PRIMARY KEY(flight_id, pass_id),"
		"FOREIGN KEY(flight_id) references flight(flight_id) "
                "on delete cascade,"
		"FOREIGN KEY(pass_id) references passenger(pass_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE pers_history("
		"flight_id int,"
		"flight_pers_id int,"
		"PRIMARY KEY(flight_id, flight_pers_id),"
		"FOREIGN KEY(flight_id) references flight(flight_id) "
                "on delete cascade,"
		"FOREIGN KEY(flight_pers_id) references flight_personnel(flight_pers_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE flight_pilot ("
		"flight_id int,"
		"pilot_id int,"
		"PRIMARY KEY(flight_id, pilot_id),"
		"FOREIGN KEY(flight_id) references flight(flight_id) "
                "on delete cascade,"
		"FOREIGN KEY(pilot_id) references pilot(pilot_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE flight_att("
		"flight_id int,"
		"att_id int,"
		"PRIMARY KEY(flight_id, att_id),"
		"FOREIGN KEY(flight_id) references flight(flight_id) "
                "on delete cascade,"
		"FOREIGN KEY(att_id) references flight_attendant(att_id) "
                "on delete cascade) ENGINE=InnoDB")

tables.append(
		"CREATE TABLE ticket("
		"ticket_id int,"
		"flight_id int,"
		"pass_id int,"
		"staff_id int,"
                "seat_no int,"
		"luggage int NOT NULL,"
		"PRIMARY KEY(ticket_id),"
		"FOREIGN KEY(flight_id, pass_id, seat_no) references reservation(flight_id, pass_id, seat_no) "
                "on delete cascade,"
		"FOREIGN KEY(staff_id) references ticket_staff(ticket_staff_id) "
                "on delete cascade) ENGINE=InnoDB")

cnt = 0
for sql in tables:
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
            print(cnt)
        pass
    else:
        print "Table successfully created"
    cnt = cnt + 1

cursor.close();
conn.close();
