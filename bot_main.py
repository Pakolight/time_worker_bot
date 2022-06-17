import telebot
import registration_enter
admin = Admin_type
bot = telebot.TeleBot('5300780935:AAGXX1j__hX2g3NA8WrMmUZtyuN1es1WcQM')




@bot.message_handler(commands= ['start'])
def start(self):
    bot.send_message(self.chat.id, "Start")


bot.polling()
