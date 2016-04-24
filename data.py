import mysql.connector

class database:
    def __init__(self, db):
        if db is None:
            raise("BANANE LAN")
        self.db = db

    def close(self):
        self.db.close()

    def check_login(self, userid, password):
        return True
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM person WHERE person_id='{}' and password='{}'".format(userid, password))
        data = cursor.fetchone()
        if data is None:
            return True
        return False

    def get_user_type(self, userid):
        return "admin"
        if userid == 0:
            return "admin"

        cursor.execute("SELECT * FROM passenger WHERE pass_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "passenger"

        cursor.execute("SELECT * FROM pilot WHERE pilot_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "pilot"

        cursor.execute("SELECT * FROM flight_attendant WHERE att_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "attendant"

        cursor.execute("SELECT * FROM store_staff WHERE store_staff_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "store_staff"

        cursor.execute("SELECT * FROM ticket_staff WHERE ticket_staff_id='{}'".format(userid))
        data = cursor.fetchone()
        if data != None:
            return "ticket_staff"
        return "nan"

if __name__ == "__main__":
    db = mysql.connector.connect(user="root", passwd="kaan")
    try:
        db.database = "airline_company"
    except mysql.connector.Error as err:
        return None
    db = database(db)

    ###### TEST CODE GOES HERE
