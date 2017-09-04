import telebot
import requests

token = '351621990:AAHxF-uSv5NLlvao4coZa6H200kAAiIA7Bo'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    global ButtonsDictionary
    ButtonsDictionary = eval(requests.get('https://raw.githubusercontent.com/P-Alban/telegrambotconfig/master/config').text)
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=1, resize_keyboard=True)
    for i in ButtonsDictionary['MainMenu']:
        if i != 'Greeting':
            markup.add(i)
    msg = bot.send_message(chat_id = message.chat.id, text = ButtonsDictionary['MainMenu']['Greeting']['text'], reply_markup=markup)
    bot.register_next_step_handler(msg, getTwoLevelButtons)

def getTwoLevelButtons(message):
    global stepMessage
    global ButtonsDictionary
    if message.text == 'About':
        getAbout(message)
    elif message.text == '/start':
        pass
    elif message.text not in ButtonsDictionary['MainMenu']:
        bot.send_message(chat_id = message.chat.id, text = 'Опция не найдена.')
        bot.register_next_step_handler(message, getTwoLevelButtons)
    else:
        stepMessage = message
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=1, resize_keyboard=True)
        for i in ButtonsDictionary['MainMenu'][message.text]:
            if i != 'Greeting':
                markup.add(i)
        markup.add('Назад')
        msg = bot.send_message(chat_id = message.chat.id, text = ButtonsDictionary['MainMenu'][message.text]['Greeting']['text'], reply_markup = markup)
        bot.register_next_step_handler(msg, getThreeLevelButtons)

def getThreeLevelButtons(message):
    global stepMessage
    global choiceName
    global ButtonsDictionary
    if message.text == 'Назад':
        send_welcome(message)
    elif message.text == '/start':
        pass
    elif message.text not in ButtonsDictionary['MainMenu'][stepMessage.text]:
        bot.send_message(chat_id = message.chat.id, text = 'Опция не найдена.')
        bot.register_next_step_handler(message, getThreeLevelButtons)
    else:
        choiceName = message
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=1, resize_keyboard=True)
        for i in ButtonsDictionary['MainMenu'][stepMessage.text][message.text]:
            if i != 'Greeting':
                markup.add(i)
        markup.add('Назад')
        msg = bot.send_message(chat_id = message.chat.id, text = ButtonsDictionary['MainMenu'][stepMessage.text][message.text]['Greeting']['text'], reply_markup = markup)
        bot.register_next_step_handler(msg, sendInstantView)

def sendInstantView(message):
    global stepMessage
    global choiceName
    global ButtonsDictionary
    if message.text == 'Назад':
        getTwoLevelButtons(stepMessage)
    elif message.text == '/start':
        pass
    else:
        if message.text not in ButtonsDictionary['MainMenu'][stepMessage.text][choiceName.text]:
            bot.send_message(chat_id = message.chat.id, text = 'Опция не найдена.')
            bot.register_next_step_handler(message, sendInstantView)
        else:
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1, resize_keyboard=True)
            markup.add('Назад')
            bot.send_message(chat_id = message.chat.id, text = 'Ссылка на Instant View: {}'.format(ButtonsDictionary['MainMenu'][stepMessage.text][choiceName.text][message.text]), reply_markup = markup)
            bot.register_next_step_handler(message, backToLevelThree)

def backToLevelThree(dirName):
    if dirName.text != '/start':
        getThreeLevelButtons(choiceName)
    else:
        pass

def getAbout(message):
    global ButtonsDictionary
    bot.send_message(chat_id = message.chat.id, text = ButtonsDictionary['MainMenu']['About']['text'])
    bot.register_next_step_handler(message, getTwoLevelButtons)

def main():
    bot.polling(none_stop = True)

if __name__ == '__main__': 
    main()