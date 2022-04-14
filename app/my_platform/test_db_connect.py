from mysql_connector import open_db_conn, close_db_conn


mydb, mycursor = open_db_conn()

sql ="INSERT INTO digital_ownership_tbl (user_info,file,embedded_watermark,hash) VALUES(%s,%s,%s,%s)"
val =("Test2","test2Picture_Pdf.png","watermark_info_2","100re2f3425r4t3")
mycursor.execute(sql,val)
mydb.commit()



#"DELETE FROM `digital_ownership_tbl` WHERE `digital_ownership_tbl`.`id` = 1"?
#mycursor.execute("DROP TABLE IF EXISTS digital_A")
#mycursor.execute("CREATE TABLE digital_A (name VARCHAR(255),product VARCHAR(255),love VARCHAR(255))")

#sql = "INSERT INTO digital_A (name,product,love) VALUES (%s,%s,%s)"
#val = ("Zipho","IQ","Top")
#mycursor.execute(sql,val)
#mydb.commit()

close_db_conn(mydb, mycursor)
#
#sql1 = "UPDATE digital_A SET love = 'THE BEST' WHERE love = 'Top'"
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
