def get_customers(db):
    cursor = db.get_db().cursor()
    #cursor.execute('''INSERT INTO customer (first_name, last_name) VALUES ('Tom B. en', 'Ska 21')''')
    #mysql.get_db().commit()
    #cursor.execute('''SHOW TABLES''')
    sql = "SELECT * FROM customer"
    cursor.execute(sql)
    result= cursor.fetchall()
    return result