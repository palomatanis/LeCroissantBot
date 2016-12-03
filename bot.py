import telebot

with open("./bot.token", "r") as token:
  bot = telebot.TeleBot(token.readline().strip()) # Strip elimina mierda que se pueda colar en el token 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # import ipdb; ipdb.set_trace()
    bot.send_message(message.chat.id, "Hola *" + message.from_user.first_name + "*!\nTe doy la bienvenida al mejor bot de la historia: Le Croissant. Disfruta la experiencia", parse_mode="Markdown")

    
# @bot.message_handler(commands=['help'])
# def send_help(message):
#     bot.send_message(message, "Howdy, how are you doing?")




print("Running....")
bot.polling()
