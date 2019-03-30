import mysql.connector

def createDB(h, u, p):
	mydb = mysql.connector.connect(
		host=h,
		user=u,
		passwd=p
	)
	return mydb