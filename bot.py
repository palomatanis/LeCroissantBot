import telebot
import json
import os
# import os.path as path


with open("./bot.token", "r") as token:
  bot = telebot.TeleBot(token.readline().strip()) # Strip elimina mierda que se pueda colar en el token 

interesados = "./data/subscribers.json"
  
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # import ipdb; ipdb.set_trace()
    bot.send_message(message.chat.id, "¡Hola *" + message.from_user.first_name + "*!\nTe doy la bienvenida al mejor bot de la historia: Le Croissant. Disfruta la experiencia", parse_mode="Markdown")

    
@bot.message_handler(commands=['subscribe'])
def send_subscr(message):
  if not os.path.isfile(interesados):
    with open(interesados, "w") as subscribers:
      subscribers.write(json.dumps([str(message.from_user.id)]))
      subscribers.close()
      bot.send_message(message.chat.id, "Has sido añadido a la lista de suscriptores a noticias sobre croissants. ¡Enhorabuena!")
  else:
    with open(interesados, "r+") as subscribersRaw:
      subscribers_list = json.load(subscribersRaw)
      if str(message.from_user.id) in subscribers_list:
        bot.send_message(message.chat.id, "Pero si ya estás en la lista, Caesa!!!!")
        subscribersRaw.close()
      else:
        subscribers_list.append(str(message.chat.id))
        bot.send_message(message.chat.id, "Has sido añadido a la lista de suscriptores a noticias sobre croissants. ¡Enhorabuena!")
        os.remove(interesados)
        with open(interesados, "w") as subscribers:
          subscribers.write(json.dumps(subscribers_list))
        subscribers.close()      
      
      
    
@bot.message_handler(commands=['croissantDay'])
def send_msssg(message):
    bot.send_message(message.chat.id, "Día de Croissants")


    
    
@bot.message_handler(commands=['unsubscribe'])
def send_goodbye(message):
    bot.send_message(message.chat.id, "Los croissants no te echarán de menos")



print("Running....")
bot.polling()
