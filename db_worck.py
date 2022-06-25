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
        connection.autocommit = True


        with connection.cursor() as cur:
                # создает табличку пользователя
                cur.execute("""CREATE TABLE IF NOT EXISTS {0}(id_name serial NOT NULL,
                                                                                       date_st date NOT NULL DEFAULT CURRENT_DATE,
                                                                                       project text NOT NULL DEFAULT CURRENT_DATE,
                                                                                       tasks text,
                                                                                       desc_ex text,
                                                                                       other_ex numeric DEFAULT 0,
                                                                                       km numeric DEFAULT 0,
                                                                                       ex numeric DEFAULT 0,
                                                                                       time_start timestamptz NOT NULL,
                                                                                       time_end timestamptz,
                                                                                       costs numeric NOT NULL DEFAULT {1},
                                                                                       arg_time numeric NOT NULL DEFAULT 3600,
                                                                                       arg_km numeric NOT NULL DEFAULT {2},
                                                                                       PRIMARY KEY (id_name) );"""
                            .format(f"{str(self.user) + '_' + str(self.id)}", f"{str(self.cost)}", f"{str(self.km)}")
                            )

        try:
            with connection.cursor() as cur:
                # put ito data from telegramm user (id and first name)
                cur.execute("""INSERT INTO list_user(user_id, user_name, pass_user) VALUES('{0}', '{1}', '{2}')"""
                            .format(f"{str(self.id)}", f"{str(self.user)}", f'{str(self.pss)}'))

        except:
            cur.close()
            connection.close()
#проверяет есть ли id пользователя в бд
class Getdate():


    def __init__(self, user_id):
        self.id = user_id


    def check_account(self):
        connection = psycopg2.connect(URI, sslmode="require")

        try:
            with connection.cursor() as cur:
                cur.execute("""SELECT user_id FROM list_user WHERE user_id = {0};"""
                            .format(f"{str(self.id)}"))

                return int(self.id) in cur.fetchone()
        except:
            return False

        finally:
            connection.close()

#Проверяет запущен ли рабочий день
    def check_start_time(self):
        connection = psycopg2.connect(URI, sslmode="require")

        try:
            with connection.cursor() as cur:
                cur.execute("""SELECT user_id FROM {0} WHERE user_id = {1};"""
                            .format(f"{'daytime_user' + '_' + str(self.id)}", f"{str(self.id)}"))

                return int(self.id) in cur.fetchone()
        except:
            return False

        finally:
            connection.close()




            #Cоздает таблицу отсчета времени рабочего дня, прои создании заносит начало рабочего дня
    def create_time_table(self):
        connection = psycopg2.connect(URI, sslmode="require")

        with connection.cursor() as cur:

            try:
                cur.execute("""CREATE TABLE IF NOT EXISTS {0} (id_name serial NOT NULL,
                                                                           date_time_st timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                                                           date_time_end timestamptz,
                                                                           project text,
                                                                           location text,
                                                                           PRIMARY KEY (id_name) );"""
                                .format(f"{'daytime_user' + '_' + str(self.id)}"))



                cur.execute("""INSERT INTO {0} (id_name) VALUES({1}) ;"""
                                .format(f"{'daytime_user' + '_' + str(self.id)}", f"{self.id}", ))
            except:

                connection.close()







#test = Getdate("580359043")
#test.create_time_table()









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