"""
1. Просим почту
    - добавляем в словарь
2. Просим пароль
    - добавляем в словарь
    - сохраняем в бд
    - создаем в бд таблицу по названию почты
3. Просим стоимость часа
    - заносим в бд стоимость часа
4. Просим стоимость км
    - заносим стоимость км в бд

"""

import telebot
import re
from loguru import logger
from db_worck import SQL_worker
from db_worck import Getdate
from db_worck import Insert
from db_worck import Details
from db_worck import List_work
from telebot.types import ReplyKeyboardMarkup as KB
from telebot.types import KeyboardButton as RB
from telebot.types import InlineKeyboardMarkup as IK
from telebot.types import InlineKeyboardButton as IB

bot = telebot.TeleBot('5300780935:AAGXX1j__hX2g3NA8WrMmUZtyuN1es1WcQM')


class Arg:
    dell = None
    data_table = None


@bot.message_handler(func=lambda msg: msg.text in {'Сancell', 'Next time'})
@bot.message_handler(commands=["start"])
def admin(self):
    # self.from_user.id
    user = Getdate(self.from_user.id)

    if user.check_account():
        key2 = KB(resize_keyboard=True, row_width=1)
        btn_1 = RB(text='Go to my account')
        btn_2 = RB(text='Sing IN to another account')
        btn_3 = RB(text='FAQ')
        key2.row(btn_1, btn_2)
        key2.row(btn_3)
        Arg.dell = bot.send_message(self.chat.id, f'Hello {self.from_user.first_name}! '
                                                  f'Good to see you again!', reply_markup=key2)

    else:
        key = KB(resize_keyboard=True, row_width=1)
        btn_1 = RB(text='Sing IN')
        btn_2 = RB(text='Sing UP')
        btn_3 = RB(text='FAQ')
        key.row(btn_1, btn_2)
        key.row(btn_3)
        Arg.dell = bot.send_message(self.chat.id, f'Hello {self.from_user.first_name}! '
                                                  f'This bot will help you calculate your working hours, '
                                                  f'wages and generate a report in a table. '
                                                  f'You can register\Sing Up or Sing In to your account',
                                    reply_markup=key
                                    )


@bot.message_handler(func=lambda msg: msg.text in {'Sing UP', 'Put in again'})
def sing_up(self):
    Arg.data_table = []
    bot.delete_message(self.chat.id, Arg.dell.id)
    call = bot.send_message(self.chat.id, 'Enter your email address', )
    bot.register_next_step_handler(call, new_user_log)
    Arg.dell = call


# check email and input all date to list "data_table"
def new_user_log(call):
    email = call.text
    result = re.findall(r"([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}", email)
    if len(result) != 0:
        bot.delete_message(call.chat.id, Arg.dell.id)
        Arg.data_table += [email, call.from_user.id, call.from_user.first_name, ]
        call = bot.send_message(call.chat.id, f'Email adres {call.text} was add\n Next enter yor pass in English')
        Arg.dell = call
        bot.register_next_step_handler(call, new_user_pass)
    else:
        bot.delete_message(call.chat.id, Arg.dell.id)
        call = bot.send_message(call.chat.id, 'Input type doesn\'t match format example.address@gmail.com')
        Arg.dell = call
        bot.register_next_step_handler(call, new_user_log)


def new_user_pass(call):
    pass_user = call.text
    result = re.findall(r"[a-z]|[A-Z]|[1-9]", pass_user)
    if len(result) != 0:
        Arg.data_table += [call.text]
        bot.delete_message(call.chat.id, Arg.dell.id)
        call = bot.send_message(call.chat.id, 'enter the cost of 1 hour of your work in the format 20.5')
        Arg.dell = call
        bot.register_next_step_handler(call, cost_hour)

    else:
        bot.delete_message(call.chat.id, Arg.dell.id)
        call = bot.send_message(call.chat.id, 'Input type doesn\'t match format please try enter password:\n'
                                              'Uppercase letters: A-Z\n'
                                              'Lowercase letters: a-z\n'
                                              'Numbers: 0-9\n'
                                              'Any of the special characters: @# $% ^ & + =\n')
        Arg.dell = call
        bot.register_next_step_handler(call, new_user_pass)


def cost_hour(call):
    Arg.data_table += [call.text]
    bot.delete_message(call.chat.id, Arg.dell.id)
    call = bot.send_message(call.chat.id, 'enter the cost of 1 km transport in the format 19.5')
    Arg.dell = call
    bot.register_next_step_handler(call, cost_km)


def cost_km(call):
    Arg.data_table += [call.text]
    mail, id, user_name, user_pass, cost_hour, cost_km = Arg.data_table

    bot.delete_message(call.chat.id, Arg.dell.id)

    key = KB(resize_keyboard=True, row_width=1)
    btn_1 = RB(text='Save')
    btn_2 = RB(text='Put in again')
    btn_3 = RB(text='Сancell')
    key.row(btn_1, btn_2)
    key.row(btn_3)

    call = bot.send_message(call.chat.id, f'Please check the information, is it correct?\n'
                                          f'Your email address: *{mail}*\n'
                                          f'your password: *{user_pass}*\n'
                                          f'The cost of 1 hour: *{cost_hour}*\n'
                                          f'The cost of 1 km transport: *{cost_km}*\n',
                            reply_markup=key, parse_mode="Markdown"
                            )
    Arg.dell = call


@bot.message_handler(func=lambda msg: msg.text == 'Save')
def sing_in(self):
    key = KB(resize_keyboard=True, row_width=1)
    btn_1 = RB(text='Go to work')
    key.row(btn_1, )
    bot.delete_message(self.chat.id, Arg.dell.id)
    mail, id, user_name, user_pass, cost_hour, cost_km = Arg.data_table
    logger.debug(f"Repack done{mail, id, user_name, user_pass, cost_hour, cost_km}", )
    sql = SQL_worker(mail, id, user_name, user_pass, cost_hour, cost_km)
    sql.enter_start_data()
    Arg.dell = bot.send_message(self.chat.id, 'Done IN', reply_markup=key)


# попадаем в меню пользователя
@bot.message_handler(func=lambda msg: msg.text in {'Go to my account', "Back", "Go to work"})
def test(self):
    bot.delete_message(self.chat.id, Arg.dell.id)
    key = KB(resize_keyboard=True, row_width=1)
    btn_1 = RB(text='Working day')
    btn_2 = RB(text='Edit data')
    btn_3 = RB(text='Output table')
    key.row(btn_1, btn_2)
    key.row(btn_3)
    Arg.dell = bot.send_message(self.chat.id, f'So  {self.from_user.first_name}! '
                                              f'Going to start. ', reply_markup=key
                                )


@bot.message_handler(func=lambda msg: msg.text == 'Working day')
def test(self):
    check = Getdate(self.from_user.id)
    if check.check_start_day():
        bot.delete_message(self.chat.id, Arg.dell.id)

        key = KB(resize_keyboard=True, row_width=1)
        btn_2 = RB(text='End the day')
        btn_3 = RB(text='Back')
        key.row(btn_2)
        key.row(btn_3)
        Arg.dell = bot.send_message(self.chat.id, f'If you\'ve finished your work day - let me know', reply_markup=key
                                    )
    else:
        key = KB(resize_keyboard=True, row_width=1)
        btn_1 = RB(text='Start the day')
        btn_3 = RB(text='Back')
        key.row(btn_1)
        key.row(btn_3)
        Arg.dell = bot.send_message(self.chat.id, f'I\'m ready to time your working day! '
                                                  f'Just press "Start the day" at the beginning of the day, '
                                                  f'and "End the day" at the end of the day. ', reply_markup=key
                                    )


@bot.message_handler(func=lambda msg: msg.text == 'Start the day')
def test(self):
    data = Getdate(self.from_user.id)
    data.create_time_table()

    bot.delete_message(self.chat.id, Arg.dell.id)

    key = KB(resize_keyboard=True, row_width=1)
    btn_2 = RB(text='End the day')
    btn_3 = RB(text='Back')
    key.row(btn_2)
    key.row(btn_3)
    Arg.dell = bot.send_message(self.chat.id, f'If you\'ve finished your work day - let me know', reply_markup=key
                                )


@bot.message_handler(func=lambda msg: msg.text == 'End the day')
def end_day(self):
    key = KB(resize_keyboard=True, row_width=1)
    btn_2 = RB(text='Enter details')
    btn_3 = RB(text='Next time')
    key.row(btn_2)
    key.row(btn_3)

    bot.delete_message(self.chat.id, Arg.dell.id)

    data = Getdate(self.from_user.id)
    data.end_day()
    data2 = Insert(self.from_user.id, self.from_user.first_name)
    data2.enter_data()
    Arg.dell = bot.send_message(self.chat.id, 'Okay, the workday is over!\n'
                                              'Culd you want to enter project details?',
                                reply_markup=key)


# Принемает данные проекта, заносит их во временную переменную
@bot.message_handler(func=lambda msg: msg.text in {'Enter details', 'Enter again'})
def details(self):
    bot.delete_message(self.chat.id, Arg.dell.id)

    call = bot.send_message(self.chat.id, "Enter project name")
    bot.register_next_step_handler(call, project_name)

    Arg.dell = call


def project_name(call):
    Arg.data_table = [call.from_user.id]
    Arg.data_table += [call.text]

    bot.delete_message(call.chat.id, Arg.dell.id)

    call = bot.send_message(call.chat.id, "Enter your tasks")
    bot.register_next_step_handler(call, tasks)

    Arg.dell = call


def tasks(call):
    Arg.data_table += [call.text]

    bot.delete_message(call.chat.id, Arg.dell.id)

    call = bot.send_message(call.chat.id, "Your distance for calculation of transport costs in km")
    bot.register_next_step_handler(call, km_total)

    Arg.dell = call

def km_total(call):
    Arg.data_table += [call.text]

    bot.delete_message(call.chat.id, Arg.dell.id)

    call = bot.send_message(call.chat.id, "Enter your expenses")
    bot.register_next_step_handler(call, expenses)

    Arg.dell = call


def expenses(call):
    Arg.data_table += [call.text]
    id, project_name, tasks, km, expenses = Arg.data_table

    bot.delete_message(call.chat.id, Arg.dell.id)

    key = KB(resize_keyboard=True, row_width=1)
    btn_1 = RB(text='Save it')
    btn_2 = RB(text='Enter again')
    btn_3 = RB(text='Сancell')
    key.row(btn_1, btn_2)
    key.row(btn_3)

    bot.send_message(call.chat.id, f'Please check the details, is it correct?\n'
                                   f'Your project_name: {project_name}\n'
                                   f'Your tasks: {tasks}\n'
                                   f'Your distance: {km}\n'
                                   f'Your expenses: {expenses}\n', reply_markup=key )

    Arg.dell = call


@bot.message_handler(func=lambda msg: msg.text == 'Save it')
def save_dates_project(self):
    # self.from_user.first_name

    save_dates_project = KB(resize_keyboard=True, row_width=1)
    btn_3 = RB(text='Back')
    save_dates_project.row(btn_3)

    id, project_name, tasks, expenses = Arg.data_table
    data = Details(self.from_user.first_name, id, project_name, tasks, expenses)
    data.insert_details()
    bot.send_message(self.chat.id, "I save it", reply_markup=save_dates_project)


#Меню редактирования листа проектов
@bot.message_handler(func=lambda msg: msg.text in {'Edit data',})
def edit_menue(self):
    edit_menue = KB(resize_keyboard=True, row_width=1)
    btn_1 = RB(text='Add new day')
    btn_2 = RB(text='Edit day')
    btn_3 = RB(text='Back')
    edit_menue.row(btn_1, btn_2)
    edit_menue.row(btn_3)

    bot.send_message(self.chat.id, "Choose what to do.", reply_markup=edit_menue,)

@bot.message_handler(func=lambda msg: msg.text in {'Edit day'})
def list_projects(self):
    data = List_work( self.from_user.first_name, self.from_user.id,)
    bot.send_message(self.chat.id, f"{data.out_list()}")

@bot.message_handler(func=lambda msg: "/edit" in msg.text )
def edit_project(self):
    Arg.data_table = []
    Arg.data_table += re.split('/edit', self.text, maxsplit=1)
    logger.info(Arg.data_table)

    edit_project = IK(row_width=1)
    kb1 = IB(text="Edit project name", callback_data="/edit_project")
    kb2 = IB(text="Edit tasks", callback_data="/edit_tasks")
    kb3 = IB(text="Edit other costs", callback_data="/edit_other_ex")
    kb4 = IB(text="Edit time start work", callback_data="/edit_time_start")
    kb5 = IB(text="Edit time end work", callback_data="/edit_time_end")
    kb6 = IB(text="Edit your distance", callback_data="/edit_km")
    edit_project.row(kb1, kb2, kb3, kb4, kb5, kb6)
    bot.send_message(self.chat.id, 'Select the editable content.', reply_markup=edit_project)

@bot.callback_query_handler(func=lambda msg: "/edit_" in msg.text):
def edit_position(self):
    Arg.data_table += re.split('/edit_', self.text, maxsplit=1)



bot.polling()
