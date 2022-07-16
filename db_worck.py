import psycopg2
import re
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

    def enter_time(self):
        try:
            with connection.cursor() as cur:
                cur.execute(""" INSERT INTO {0}(time_start, time_end)
                                SELECT date_time_st, date_time_end
                                FROM {1}
                                WHERE id_name = {2};"""
                            .format(f'{str(self.user) + "_" + str(self.id)}',
                                    f"{'daytime_user' + '_' + str(self.id)}",
                                    f'{str(self.id)}'))

                logger.info("Добавил время в основную таблицу, создал в ней строку")
                connection.commit()

        except:
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

                return cur.fetchone()
        except:
            return False

        finally:
            connection.close()

#Проверяет запущен ли рабочий день, создана ли таблица


    def check_start_day(self):
        connection = psycopg2.connect(URI, sslmode="require")

        try:
            with connection.cursor() as cur:
                    cur.execute("""SELECT date_time_st FROM {0};"""
                            .format(f"{'daytime_user' + '_' + str(self.id)}",))
            return cur.fetchone

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
                                                                           date_time_st timestamptz 
                                                                           NOT NULL DEFAULT CURRENT_TIMESTAMP+'02:00',
                                                                           date_time_end timestamptz,
                                                                           project text,
                                                                           location text,
                                                                           PRIMARY KEY (id_name) );"""
                                .format(f"{'daytime_user' + '_' + str(self.id)}"))

                connection.commit()
                cur.execute("""INSERT INTO {0} (id_name) VALUES({1}) ;"""
                                .format(f"{'daytime_user' + '_' + str(self.id)}", f"{self.id}", ))
                connection.commit()
            except:

                connection.close()

    def end_day(self):

        connection = psycopg2.connect(URI, sslmode="require")

        try:
            with connection.cursor() as cur:
                cur.execute(""" UPDATE {0} SET date_time_end = CURRENT_TIMESTAMP+'02:00';"""
                            .format(f"{'daytime_user' + '_' + str(self.id)}", ))
                logger.info("Добавид время оканчания")
                connection.commit()
        except:
            connection.close()

#Вставляет данные с временной таблицы времени, в табл проектов и удаляет временную таблицу.
class Insert():
    def __init__(self, user_id, user_name,):
        self.id = user_id
        self.user = user_name

    def enter_data(self):
        connection = psycopg2.connect(URI, sslmode="require")

        try:
            with connection.cursor() as cur:
                cur.execute(""" INSERT INTO {0} (time_start, time_end)
                                SELECT date_time_st, date_time_end
                                FROM {1}
                                ;"""
                            .format(f"{str(self.user) + '_' + str(self.id)}",
                                    f"{'daytime_user' + '_' + str(self.id)}",
                                    ))

                logger.info("Добавид в основную табл данные с временной")
                connection.commit()

        except:
                connection.close()

        connection = psycopg2.connect(URI, sslmode="require")

        try:
            with connection.cursor() as cur:
                cur.execute(""" DROP TABLE {0};"""
                            .format(f"{'daytime_user' + '_' + str(self.id)}", ))
                connection.commit()

        except:
            connection.close()

    def add_data(self):
            connection = psycopg2.connect(URI, sslmode="require")

            try:
                with connection.cursor() as cur:
                    cur.execute(""" INSERT INTO {0} (project, time_start) VALUES ('New Project', CURRENT_TIMESTAMP+'02:00')
                                    ;"""
                                .format(f"{str(self.user) + '_' + str(self.id)}",
                                        f"{'daytime_user' + '_' + str(self.id)}",
                                        ))

                    logger.info("Добавид в основную табл данные '1' ")
                    connection.commit()

            except:
                    connection.close()

class Details():

    def __init__(self, user, id, project_name, tasks, km, expenses):
        self.user = user
        self.id = id
        self.project_name = project_name
        self.tasks = tasks
        self.km = km
        self.expenses = expenses
#Определяет последний проект по id чекает самый большой
    def lust_project(self):
        connection = psycopg2.connect(URI, sslmode="require")

        with connection.cursor() as cur:
            cur.execute(""" SELECT id_name FROM {0};""".format(f"{str(self.user) + '_' + str(self.id)}",))

            arg = cur.fetchall()
            return max(arg[0])

    def insert_details(self):
        connection = psycopg2.connect(URI, sslmode="require")
        id_project = self.lust_project()
        try:
            with connection.cursor() as cur:
                cur.execute(""" UPDATE {0}
                                SET project='{1}', tasks='{2}', km={3} other_ex={4},
                                WHERE id_name={5};"""
                            .format(f"{str(self.user) + '_' + str(self.id)}",
                                    f"{self.project_name}",
                                    f"{self.tasks}",
                                    f"{self.km}",
                                    f"{self.expenses}",
                                    f"{int(id_project)}"))
                connection.commit()
        except:
            connection.close()

class List_work():


    time_arg = None

    def __init__(self, user, id,):
        self.user = user
        self.id = id

    def out_list(self):
        logger.info("ime in out_list")
        connection = psycopg2.connect(URI, sslmode="require")
        try:
            with connection.cursor() as cur:
                cur.execute(""" SELECT id_name, project 
                                FROM {0} ;"""
                            .format(f"{str(self.user) + '_' + str(self.id)}",))
                arg = cur.fetchall()
                logger.info(arg)
                text = "List projects:"
                for i in arg:
                    text += f"\n{i[0]} /i{i[0]}  {i[1]}   /edit{i[0]} /dell{i[0]}"
                logger.info(text)
                if text == "List projects:":
                    return f"Sorry {str(self.user)} you have no added dates."
                else:
                    return text
        except:
            return f"Sorry {str(self.user)} you have no added dates."

        finally:
            connection.close()

    def out_info(self, id_name):
        connection = psycopg2.connect(URI, sslmode="require")
        try:
            with connection.cursor() as cur:
                cur.execute(""" update {0}
                                    set ex = (km * arg_km) + other_ex;"""
                            .format(f"{str(self.user) + '_' + str(self.id)}",))
                connection.commit()

            with connection.cursor() as cur:
                cur.execute(""" SELECT date_st, project, tasks, time_start, time_end, 
                                time_end - time_start as duration, desc_ex, km, km * arg_km as km_cost , other_ex, ex, 
                                (((to_number(to_char((time_end - time_start), 'ssss'  ), '99999') * costs) / arg_time ) + ex ) 
                                AS price from {0} WHERE id_name={1};"""
                            .format(f"{str(self.user) + '_' + str(self.id)}", id_name[1]))
                arg = cur.fetchone()
        except:
            connection.close()

        time_st = re.sub(r'\+00:00', '', f'{arg[3]}')
        time_end = re.sub(r'\+00:00', '', f'{arg[4]}')
        logger.info(arg[0])
        return f"Data: {arg[0]}\n" \
               f"Project: {arg[1]}\n" \
               f"Tasks: {arg[2]}\n" \
               f"Time start: {time_st}\n" \
               f"Time end: {time_end}\n" \
               f"Duration: {arg[5]}\n" \
               f"Km: {arg[7]}\n" \
               f"other_ex: {arg[8]}\n" \
               f"Ex: {arg[9]}\n" \
               f"Total: {round(float(arg[11]), 1)}\n" \

    def dell (self, id_name):
        connection = psycopg2.connect(URI, sslmode="require")
        try:
            logger.info(id_name)
            with connection.cursor() as cur:
                cur.execute(""" DELETE FROM {0}
                                where id_name = {1};"""
                            .format(f"{str(self.user) + '_' + str(self.id)}", id_name[1]))

                connection.commit()
                return f"Dellet project {id_name[1]} is done."
        except:
            return f"Error List_work.dell() "

        finally:
            connection.close()

    def lust_project(self):
        connection = psycopg2.connect(URI, sslmode="require")

        with connection.cursor() as cur:
            cur.execute(""" SELECT id_name FROM {0};""".format(f"{str(self.user) + '_' + str(self.id)}",))

            arg = cur.fetchall()
            return max(arg[0])

    def dell_all_date (self,):
        connection = psycopg2.connect(URI, sslmode="require")
        try:
            with connection.cursor() as cur:
                cur.execute("""TRUNCATE TABLE {0};"""
                            .format(f"{str(self.user) + '_' + str(self.id)}", ))

                connection.commit()
                return f"Dellet all data is done."
        except:
            return f"Error dell_all_date() "


class Edit():
    def __init__(self, user, id, id_name, arg, text):
        self.user = user
        self.id = id
        self.arg = arg
        self.id_name = id_name
        self.text = text

    def edit_row(self):
        connection = psycopg2.connect(URI, sslmode="require")

        try:
            with connection.cursor() as cur:
                cur.execute("""UPDATE {0}
                               SET {1} ='{2}'
                               WHERE id_name = {3};"""
                            .format(f"{str(self.user) + '_' + str(self.id)}",
                                    f"{self.arg}",
                                    f"{self.text}",
                                    f"{self.id_name}"))
            connection.commit()
            return "Change made!"
        except:
            return "Data entry error!\n " \
                   "Enter cost in the form 12.00\n " \
                   "Start time in the form 2022-07-01 11:35:25.00 +00"

        finally:
            connection.close()

class Out_pdf():

    arg = None
    time_arg = None
    add_arg = [
        ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other",
         "Total", "Price"],
    ]

    def __init__(self, user, id,):
        self.user = user
        self.id = id

    def arg_for_pdf(self):
        self.add_arg = [
            ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other",
             "Total", "Price"],
        ]
        try:
            with connection.cursor() as cur:

                cur.execute(""" update {0}
                                set ex = (km * arg_km) + other_ex;
                                SELECT  date_st, project, tasks, time_start, 
                                        time_end,time_end - time_start as duration, 
                                        desc_ex, km, km * arg_km as km_cost ,  
                                        other_ex, ex,                             
                            (((to_number(to_char((time_end - time_start), 'ssss'  ), '99999') * costs) / arg_time ) + ex ) as price
                                        from {0}; """.format(f"{str(self.user) + '_' + str(self.id)}", )
                            )

                Out_pdf.arg = iter(cur.fetchall())
        except:
            connection.close()
            logger.debug("in argument pdf")

    def update(self):
        try:
            self.time_arg = next(self.arg)
            logger.debug("True")
            return True

        except StopIteration:
            logger.debug("False")
            return False

    def date(self):
        return str(self.time_arg[0])

    def project(self):
        return str(self.time_arg[1])

    def tasks(self):
        return str(self.time_arg[2])

    def time_start(self):
        text = str(self.time_arg[3])
        result = re.split("\:\d{2}\.\d{6}\+\d{2}:\d{2}|\:\d{2}\+\d{2}\:\d{2}", text, maxsplit=1)
        return str(result[0])

    def time_end(self):
        text = str(self.time_arg[4])
        result = re.split("\:\d{2}\.\d{6}\+\d{2}:\d{2}|\:\d{2}\+\d{2}\:\d{2}", text, maxsplit=1)
        return str(result[0])

    def duration(self):
        text = str(self.time_arg[5])
        result = re.split("\:\d{2}\.\d{5}", text, maxsplit=1)
        return str(result[0])

    def d_ex(self):
        return str(self.time_arg[6])

    def km(self):
        return str(self.time_arg[7])

    def km_cost(self):
        return str(self.time_arg[8])

    def o_ex(self):
        return str(self.time_arg[9])

    def ex(self):
        return str(self.time_arg[10])

    def price(self):
        return str(round(float(self.time_arg[11]), 1))


    def creat(self):
        if self.update():
            self.add_arg.append([self.date(),
                                 self.date(),
                                 self.tasks(),
                                 self.time_start(),
                                 self.time_end(),
                                 self.duration(),
                                 self.d_ex(),
                                 self.km(),
                                 self.km_cost(),
                                 self.o_ex(),
                                 self.ex(),
                                 self.price(),
                                 ])
            logger.info(f"Eteration\n" )
            self.creat()

        else:
            return(self.add_arg)

    def out(self):
        self.creat()
        logger.info(self.add_arg)
        return self.add_arg

class Out_pdf_smal():

    arg = None
    time_arg = None
    add_arg = [
        ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other",
         ],
    ]

    def __init__(self, user, id,):
        self.user = user
        self.id = id

    def arg_for_pdf(self):
        self.add_arg = [
            ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other",
             "Total",],
        ]
        try:
            with connection.cursor() as cur:

                cur.execute(""" update {0}
                                set ex = (km * arg_km) + other_ex;
                                SELECT  date_st, project, tasks, time_start, 
                                        time_end,time_end - time_start as duration, 
                                        desc_ex, km, km * arg_km as km_cost ,  
                                        other_ex, ex,                             
                            (((to_number(to_char((time_end - time_start), 'ssss'  ), '99999') * costs) / arg_time ) + ex ) as price
                                        from {0}; """.format(f"{str(self.user) + '_' + str(self.id)}", )
                            )

                Out_pdf_smal.arg = iter(cur.fetchall())
        except:
            connection.close()
            logger.debug("in argument pdf")

    def update(self):
        try:
            self.time_arg = next(self.arg)
            logger.debug("True")
            return True

        except StopIteration:
            logger.debug("False")
            return False

    def date(self):
        return str(self.time_arg[0])

    def project(self):
        return str(self.time_arg[1])

    def tasks(self):
        return str(self.time_arg[2])

    def time_start(self):
        text = str(self.time_arg[3])
        result = re.split("\:\d{2}\.\d{6}\+\d{2}:\d{2}|\:\d{2}\+\d{2}\:\d{2}", text, maxsplit=1)
        return str(result[0])

    def time_end(self):
        text = str(self.time_arg[4])
        result = re.split("\:\d{2}\.\d{6}\+\d{2}:\d{2}|\:\d{2}\+\d{2}\:\d{2}", text, maxsplit=1)
        return str(result[0])

    def duration(self):
        text = str(self.time_arg[5])
        result = re.split("\:\d{2}\.\d{5}", text, maxsplit=1)
        return str(result[0])

    def d_ex(self):
        return str(self.time_arg[6])

    def km(self):
        return str(self.time_arg[7])

    def km_cost(self):
        return str(self.time_arg[8])

    def o_ex(self):
        return str(self.time_arg[9])

    def ex(self):
        return str(self.time_arg[10])



    def creat(self):
        if self.update():
            self.add_arg.append([self.date(),
                                 self.date(),
                                 self.tasks(),
                                 self.time_start(),
                                 self.time_end(),
                                 self.duration(),
                                 self.d_ex(),
                                 self.km(),
                                 self.km_cost(),
                                 self.o_ex(),
                                 self.ex(),
                                 ])
            logger.info(f"Eteration\n" )
            self.creat()

        else:
            return(self.add_arg)

    def out(self):
        self.creat()
        return self.add_arg












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