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
from db_worck import SQL_worker
from telebot.types import ReplyKeyboardMarkup as KB
from telebot.types import KeyboardButton as RB

bot = telebot.TeleBot('5300780935:AAGXX1j__hX2g3NA8WrMmUZtyuN1es1WcQM')
sql = SQL_worker
users_id = ["580359043"]

class Arg:
    dell = None
    data_table = None


@bot.message_handler(func=lambda msg: msg.text in {'Сancell'})
@bot.message_handler(commands=["start"])
def admin(self):
    if self.from_user.id not in users_id:
        key = KB(resize_keyboard=True, row_width=1)
        btn_1 = RB(text='Sing IN')
        btn_2 = RB(text='Sing UP')
        btn_3 = RB(text='FAQ')
        key.row(btn_1, btn_2)
        key.row(btn_3)
        Arg.dell = bot.send_message(self.chat.id, f'Hello {self.from_user.first_name}! '
                                       f'This bot will help you calculate your working hours, '
                                       f'wages and generate a report in a table. '
                                       f'You can register\Sing Up or Sing In to your account', reply_markup=key
                         )

    else:
        Arg.dell = bot.send_message(self.chat.id, f'Hello {self.from_user.first_name}! '
                                       f'Good to see you again!')


@bot.message_handler(func=lambda msg: msg.text in {'Sing UP', 'Put in again'})
def sing_up(self):
    Arg.data_table = []
    bot.delete_message(self.chat.id, Arg.dell.id)
    call = bot.send_message(self.chat.id, 'Enter your email address',)
    bot.register_next_step_handler(call, new_user_log)
    Arg.dell = call

#check email and input all date to list "data_table"
def new_user_log(call):
    bot.delete_message(call.chat.id, Arg.dell.id)
    email = call.text
    result = re.findall(r"([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}", email)
    if len(result) != 0:
        Arg.data_table += [email, call.from_user.id, call.from_user.first_name,]
        call = bot.send_message(call.chat.id, f'Email adres {call.text} was add\n Next enter yor pass in English')
        Arg.dell = call
        bot.register_next_step_handler(call, new_user_pass)
    else:
        bot.delete_message(call.chat.id, Arg.dell.id)
        call = bot.send_message(call.chat.id, 'Input type doesn\'t match format example.address@gmail.com')
        Arg.dell = call
        bot.register_next_step_handler(call, new_user_log)

def new_user_pass(call):
    Arg.data_table += [call.text]
    bot.delete_message(call.chat.id, Arg.dell.id)
    call = bot.send_message(call.chat.id, 'enter the cost of 1 hour of your work in the format 20.5')
    Arg.dell = call
    bot.register_next_step_handler(call, cost_hour)

def cost_hour(call):
    Arg.data_table += [call.text]
    bot.delete_message(call.chat.id, Arg.dell.id)
    call = bot.send_message(call.chat.id, 'enter the cost of 1 km transport in the format 19.5')
    Arg.dell = call
    bot.register_next_step_handler(call, cost_km)

def cost_km(call):
    Arg.data_table += [call.text]
    mail, user_pass, cost_hour, cost_km = Arg.data_table
    bot.delete_message(call.chat.id, Arg.dell.id)

    key = KB(resize_keyboard=True, row_width=1)
    btn_1 = RB(text='Save it')
    btn_2 = RB(text='Put in again')
    btn_3 = RB(text='Сancell')
    key.row(btn_1, btn_2)
    key.row(btn_3)

    call = bot.send_message(call.chat.id, f'Please check the information, is it correct?'
                                          f'Your email address: {mail}\n'
                                          f'your password: {user_pass}\n'
                                          f'The cost of 1 hour: {cost_hour}\n'
                                          f'The cost of 1 km transport{cost_km}\n',
                            reply_markup=key
                            )
    Arg.dell = call
    bot.register_next_step_handler(call, cost_km)

@bot.message_handler(func=lambda msg: msg.text == 'Save it')
def sing_in(self):
    mail, user_pass, cost_hour, cost_km = Arg.data_table
    add = sql(mail, user_pass, cost_hour, cost_km)
    add.enter_start_data()
    bot.send_message(self.chat.id, 'Done IN')

# Вариант с функцией и с импортом re

@bot.message_handler(func=lambda msg: msg.text == 'Sing IN')
def sing_in(self):
    bot.send_message(self.chat.id, 'Done IN')




bot.polling()
