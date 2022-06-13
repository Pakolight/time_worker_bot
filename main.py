import psycopg2
from loguru import logger
from config import URI

connection = psycopg2.connect(URI, sslmode="require")
connection.autocommit = True

with connection.cursor() as cur:
    cur.execute("""CREATE TABLE IF NOT EXISTS timelist(id_name serial NOT NULL,
                                                       date_st date NOT NULL DEFAULT CURRENT_DATE,
                                                       project text NOT NULL DEFAULT CURRENT_DATE, 
                                                       tasks text, 
                                                       desc_ex text, 
                                                       other_ex numeric DEFAULT 0, 
                                                       km numeric DEFAULT 0, 
                                                       ex numeric DEFAULT 0, 
                                                       time_start time NOT NULL, 
                                                       time_end time, 
                                                       costs numeric NOT NULL DEFAULT 12, 
                                                       arg_time numeric NOT NULL DEFAULT 3600, 
                                                       arg_km numeric NOT NULL DEFAULT 0.19, 
                                                       PRIMARY KEY (id_name) );"""
                )

    cur.execute(""" update timelist
                    set ex = (km * arg_km) + other_ex;
                    SELECT  date_st, project, tasks, time_start, 
                            time_end,time_end - time_start as duration, 
                            desc_ex, km, km * arg_km as km_cost ,  
                            other_ex, ex,                             
                (((to_number(to_char((time_end - time_start), 'ssss'  ), '99999') * costs) / arg_time ) + ex ) as price
                            from timelist; """
                )
    x = cur.fetchone()
    print(x)

    logger.debug("done")



