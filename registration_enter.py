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
from telebot.types import ReplyKeyboardMarkup as KB
from telebot.types import KeyboardButton as RB

bot = telebot.TeleBot('5300780935:AAGXX1j__hX2g3NA8WrMmUZtyuN1es1WcQM')

users_id = ["580359043"]

class Arg:
    dell = None



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


@bot.message_handler(func=lambda msg: msg.text == 'Sing UP')
def sing_up(self):
    bot.delete_message(self.chat.id, Arg.dell.id)
    call = bot.send_message(self.chat.id, 'Enter your email address',)
    bot.register_next_step_handler(call, new_user_log)
    Arg.dell = call

def new_user_log(call):
    text = call.text
    result = re.findall(r"([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}", text)
    if len(result) != 0:
        bot.send_message(call.chat.id, 'Это номер')
    else:
        bot.send_message(call.chat.id, 'Введите номер')


# Вариант с функцией и с импортом re

@bot.message_handler(func=lambda msg: msg.text  == 'Sing IN')
def sing_in(self):
    bot.send_message(self.chat.id, 'Done IN')




bot.polling()
