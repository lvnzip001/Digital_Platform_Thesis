import mysql.connector

def open_db_conn():
    mydb = mysql.connector.connect(
        host='bx4awsynv0pkp8jdrbat-mysql.services.clever-cloud.com',
        user='uiw8j2jyla8jzpok',
        passwd='GShJY1w0tqjMYx4t3gek',
        database='bx4awsynv0pkp8jdrbat'
    )

    print(mydb)
    mycursor = mydb.cursor()
    return(mydb,mycursor)




##mycursor.execute("DROP TABLE IF EXISTS digital_resources")
##mycursor.execute("CREATE TABLE digital (name VARCHAR(255),product VARCHAR(255),love VARCHAR(255))")
#
#sql = "INSERT INTO digital (name,product,love) VALUES (%s,%s,%s)"
#val = ("Zipho","IQ","Top")
#mycursor.execute(sql,val)
#mydb.commit()
#
#sql1 = "UPDATE digital SET love = 'THE BEST' WHERE love = 'Top'"
#
#mycursor.execute(sql1)
#mydb.commit()
#
#sql2 = " SELECT * FROM digital WHERE love = 'THE BEST'"
#mycursor.execute(sql2)
#myresult = mycursor.fetchall()
#
#for result in myresult:
#    print(result)
#
#sql3 = "DELETE FROM digital WHERE name = 'Zipho' "
#
#mycursor.execute(sql3)
#mydb.commit()
def close_db_conn(mydb, mycursor):
    mycursor.close()
    mydb.close()