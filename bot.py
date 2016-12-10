import telebot
from telebot import types
import json
import os
# import os.path as path

# activated = true

# Abrir cosas

with open("./bot.token", "r") as token:
  bot = telebot.TeleBot(token.readline().strip()) # Strip elimina mierda que se pueda colar en el token 


with open('./data/admins.json', 'r') as adminData:
    admins = json.load(adminData)


    
adictos_a_croissants = "./data/subscribers.json"



def isAdmin_fromPrivate(message):
    if message.chat.type == 'private':
        userID = message.from_user.id
        if str(userID) in admins:
            return True
        return False

def replyToQuestion(adict):
  markup = types.ReplyKeyboardMarkup()
  markup.one_time_keyboard = True
  markup.row('¡SÍ!')
  markup.row('¡NO, PESADA!')
  bot.send_message(adict, "¿Croissant?", reply_markup=markup)
  


      
def notificarAdictos():
  with open(adictos_a_croissants, "r+") as subscribersRaw:
      subscribers_list = json.load(subscribersRaw)
  [replyToQuestion(adict) for adict in subscribers_list]
  
  return


### cosas de comandos
      
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # import ipdb; ipdb.set_trace()
  bot.send_message(message.chat.id, "¡Hola *" + message.from_user.first_name + "*!\nTe doy la bienvenida al mejor bot de la historia: Le Croissant. Disfruta la experiencia\n/help", parse_mode="Markdown")

  
# Lista de comandos      
@bot.message_handler(commands=['help'])
def send_help(message):
  bot.send_message(message.chat.id, "Hola!\n Los comandos que puedes usar son:\n/help\n/subscribe\n/horario\n/unsubscribe")
  
@bot.message_handler(commands=['subscribe'])
def send_subscr(message):
  if not os.path.isfile(adictos_a_croissants):
    with open(adictos_a_croissants, "w") as subscribers:
      subscribers.write(json.dumps([str(message.from_user.id)]))
      subscribers.close()
      bot.send_message(message.chat.id, "Has sido añadido a la lista de suscriptores a noticias sobre croissants. ¡Enhorabuena!")
  else:
    with open(adictos_a_croissants, "r+") as subscribersRaw:
      subscribers_list = json.load(subscribersRaw)
      if str(message.from_user.id) in subscribers_list:
        bot.send_message(message.chat.id, "Pero si ya estás en la lista, Caesa!!!!")
        print (message.from_user.id)
        subscribersRaw.close()
      else:
        subscribers_list.append(str(message.chat.id))
        bot.send_message(message.chat.id, "Has sido añadido a la lista de suscriptores a noticias sobre croissants. ¡Enhorabuena!")
        os.remove(adictos_a_croissants)
        with open(adictos_a_croissants, "w") as subscribers:
          subscribers.write(json.dumps(subscribers_list))
        subscribers.close()      
       

# Esto aun no sirve de nada pero me gusta el nombre
@bot.message_handler(commands=['croissantDay'])
def send_msssg(message):
    bot.send_message(message.chat.id, "Día de Croissants")


# Horario de la panadería
@bot.message_handler(commands=['horario'])
def horarios(message):
    bot.send_message(message.chat.id, "Horario de la Panadería:\nLunes - Viernes: 07:30 - 21:30\nSábados: 09:00 - 16:00\nDomingos y festivos: 09:00 - 21:00")

  
# Ya se verá si se implementa esto algún día, por ahora supongo que nadie querrá salir de la lista nunca.    
@bot.message_handler(commands=['unsubscribe'])
def send_goodbye(message):
    bot.send_message(message.chat.id, "Los croissants no te echarán de menos\n\n(de todas maneras esta función no está implementada..ups)")


# Cuando un admin va a ir a la Panadería, esto notifica a todos los suscriptores.
@bot.message_handler(commands=['croissant'])
def croissant_notif(message):
    if isAdmin_fromPrivate(message):
      bot.reply_to(message,
                   "Lanzando ofrecimiento de dulce felicidad en forma de Croissant Supremo...")
      
      notificarAdictos()
    else:
      bot.reply_to(message, "No intentes suplantar al proveedor de Croissants")



print("Running....")
bot.polling()
