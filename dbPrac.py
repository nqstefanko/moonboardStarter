import dbUtil

mydb = dbUtil.createDB("localhost", "root", "pass")
print(mydb)

mycursor = mydb.cursor()

mycursor.execute("SELECT name, setterGrade FROM moondb.problems2016 WHERE setterGrade='8b+'")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
#mycursor = mydb.cursor()

