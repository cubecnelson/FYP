import re
import MySQLdb


db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="root", # your password
                      db="crux") # name of the data base



cursor = db.cursor()

cursor.execute("""SELECT CONTENT FROM `crux`.`tweets`""")
	    
records = cursor.fetchall()

counts = dict()

for record in records:
	tags = re.findall(r"#(\w+)", str(record))
	if tags:
		for tag in tags:
			try:
				counts[str(tag)] = counts[str(tag)] + 1
			except KeyError:
				counts[str(tag)] = 1

f = open("hashtag_count", "wb")

for key, value in counts.items():
    f.write( key + "\t" + str(value) + "\n")