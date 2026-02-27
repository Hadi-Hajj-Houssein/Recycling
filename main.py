import psycopg2
from models.user import User

connector  = psycopg2.connect(host = "localhost", db_name = "Recycling" ,user = "postgres", password = "123", port ="5432") #  host db name user password port 


curs = connector.cursor() # to insert detyte ne5tere3 table  upd
curs.execute(User) # bi 8er file 
connector.commit()
connector.close()
curs.close()