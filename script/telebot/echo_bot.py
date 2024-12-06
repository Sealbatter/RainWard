import telebot

bot = telebot.TeleBot('7915806680:AAE9KEt_YStlFDg4kEeMBZA1NuADndAVQCk'
                      , parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()