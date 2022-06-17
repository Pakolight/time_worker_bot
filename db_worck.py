import psycopg2
from loguru import logger
from config import URI


class sql_worker():
    connection = psycopg2.connect(URI, sslmode="require")
    connection.autocommit = True

    def __init__(self, email, user_id, user_pass, cost_hour, km):
        self.em = email
        self.id = user_id
        self.pss = user_pass
        self.cost = cost_hour
        self.km = km

    # Создает таблицу по с названием почты, заносит данные юзера в таблицу
    def enter_start_data(self):

        try:
            with connection.cursor() as cur:
                # создает табличку пользователя
                cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.em}(id_name serial NOT NULL,
                                                                       date_st date NOT NULL DEFAULT CURRENT_DATE,
                                                                       project text NOT NULL DEFAULT CURRENT_DATE,
                                                                       tasks text,
                                                                       desc_ex text,
                                                                       other_ex numeric DEFAULT 0,
                                                                       km numeric DEFAULT 0,
                                                                       ex numeric DEFAULT 0,
                                                                       time_start time NOT NULL,
                                                                       time_end time,
                                                                       costs numeric NOT NULL DEFAULT {self.cost},
                                                                       arg_time numeric NOT NULL DEFAULT 3600,
                                                                       arg_km numeric NOT NULL DEFAULT {self.km},
                                                                       PRIMARY KEY (id_name) );"""
                            )
        except:
            cur.close()
            connection.close()
            logger.debug("close")

        try:
            with connection.cursor() as cur:
                # создает табличку
                cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.em}(id_name serial NOT NULL,
                                                                       date_st date NOT NULL DEFAULT CURRENT_DATE,
                                                                       project text NOT NULL DEFAULT CURRENT_DATE,
                                                                       tasks text,
                                                                       desc_ex text,
                                                                       other_ex numeric DEFAULT 0,
                                                                       km numeric DEFAULT 0,
                                                                       ex numeric DEFAULT 0,
                                                                       time_start time NOT NULL,
                                                                       time_end time,
                                                                       costs numeric NOT NULL DEFAULT {self.cost},
                                                                       arg_time numeric NOT NULL DEFAULT 3600,
                                                                       arg_km numeric NOT NULL DEFAULT {self.km},
                                                                       PRIMARY KEY (id_name) );"""
                            )
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
    logger.debug("close")
