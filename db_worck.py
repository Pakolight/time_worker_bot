import psycopg2
from loguru import logger
from config import URI
connection = psycopg2.connect(URI, sslmode="require")
connection.autocommit = True

class SQL_worker():

    def __init__(self, email, user_id, user_name, user_pass, cost_hour, km):
        self.em = email
        self.id = user_id
        self.user = user_name
        self.pss = user_pass
        self.cost = cost_hour
        self.km = km

    # Создает таблицу по с названием почты, заносит данные юзера в таблицу
    def enter_start_data(self):
        connection = psycopg2.connect(URI, sslmode="require")
        #connection.autocommit = True

        try:
            with connection.cursor() as cur:
                logger.debug(f"i'am in SQL{self.em}")
                # создает табличку пользователя
                cur.execute("""CREATE TABLE IF NOT EXISTS {0}(id_name serial NOT NULL,
                                                                       date_st date NOT NULL DEFAULT CURRENT_DATE,
                                                                       project text NOT NULL DEFAULT CURRENT_DATE,
                                                                       tasks text,
                                                                       desc_ex text,
                                                                       other_ex numeric DEFAULT 0,
                                                                       km numeric DEFAULT 0,
                                                                       ex numeric DEFAULT 0,
                                                                       time_start time NOT NULL,
                                                                       time_end time,
                                                                       costs numeric NOT NULL DEFAULT {1},
                                                                       arg_time numeric NOT NULL DEFAULT 3600,
                                                                       arg_km numeric NOT NULL DEFAULT {2},
                                                                       PRIMARY KEY (id_name) );"""
                            .format(f"{self.em}", f"{self.cost}", f"{self.km}")
                            )
                connection.commit()
        except:
            cur.close()
            connection.close()
            logger.debug("close")

        try:
            with connection.cursor() as cur:
                # put ito data from telegramm user (id and first name)
                cur.execute("""INSERT INTO list_user(user_id, user_name) VALUES('{0}', '{1}',)"""
                            .format(f"{self.id}", f"{self.user}"))
                connection.commit()

        except:
            cur.close()
            connection.close()
            logger.debug("close")

'''
try:
    with connection.cursor() as cur:

        cur.execute(""" update timelist
                        set ex = (km * arg_km) + other_ex;
                        SELECT  date_st, project, tasks, time_start, 
                                time_end,time_end - time_start as duration, 
                                desc_ex, km, km * arg_km as km_cost ,  
                                other_ex, ex,                             
                    (((to_number(to_char((time_end - time_start), 'ssss'  ), '99999') * costs) / arg_time ) + ex ) as price
                                from timelist; """
                    )

        args_all = cur.fetchall()
except:
    cur.close()
    connection.close()
    logger.debug("close")

try:
    with connection.cursor() as cur:

        cur.execute(""" update timelist
                        set ex = (km * arg_km) + other_ex;
                        SELECT  date_st, project, tasks, time_start, 
                                time_end,time_end - time_start as duration, 
                                desc_ex, km, km * arg_km as km_cost ,  
                                other_ex, ex,                             
                    (((to_number(to_char((time_end - time_start), 'ssss'  ), '99999') * costs) / arg_time ) + ex ) as price
                                from timelist; """
                    )

        args_all = cur.fetchall()
except:
    cur.close()
    connection.close()

'''