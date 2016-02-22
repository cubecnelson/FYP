import mysql.connector

config = {
	'host': 'localhost',
	'port': 3306,
	'database': 'test',
	'user': 'root',

}

db = mysql.connector.Connect(**config)
cursor = db.cursor()
cursor.execute('CREATE TABLE MyGuests (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,firstname VARCHAR(30) NOT NULL,lastname VARCHAR(30) NOT NULL,email VARCHAR(50),reg_date TIMESTAMP)')