def get_customers(db):
    cursor = db.get_db().cursor()
    sql = "SELECT * FROM customer"
    cursor.execute(sql)
    result= cursor.fetchall()
    return result

def add_customer(db,first_name,last_name,email, password1):
    cursor = db.get_db().cursor()
    sql = f"INSERT INTO customer (first_name, last_name, email, password1) VALUES ({first_name}, {last_name}, {email}, {password1})"
    cursor.execute(sql)