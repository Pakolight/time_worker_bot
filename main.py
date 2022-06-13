import psycopg2
from loguru import logger
from config import URI


connection = psycopg2.connect(URI, sslmode="require")
connection.autocommit = True

with connection.cursor() as cur:


'''
    #создает табличку
    cur.execute('CREATE TABLE timelist(id_name serial NOT NULL, '
                'date_st date NOT NULL DEFAULT CURRENT_DATE, '
                'project text NOT NULL DEFAULT CURRENT_DATE, '
                'tasks text, '
                'desc_ex text, '
                'ex numeric DEFAULT 0, '
                'time_start time NOT NULL, '
                'time_end time, '
                'costs numeric NOT NULL DEFAULT 12, '
				'arg numeric NOT NUL DEFAULT 3600, '
                'PRIMARY KEY (id_name));')
                
    #заносит данные в базу
    #cur.execute("""INSERT INTO timelist(time_start, time_end, ex) VALUES('9:30', '18:00', '10')""")

    
'''








