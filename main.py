import telebot
from config import TOKEN, keys
from extensions import ValutaException, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'правила пользования ботом. отправьте сообщение боту в виде\n<имя валюты, цену которой хотите узнать>\n\
    <имя валюты, в которой надо узнать цену первой валюты>\n<количество первой валюты>\n\
    например: биткойн доллар 1\n\
    помощь /help\nсписок доступных валютов /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ValutaException('Слишком много параметров')
        base, quote, amount = values
        total_quote = ValutaConverter.convert(quote, base, amount)
    except ValutaException as e:
        bot.reply_to(message, f'ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_quote}'
        bot.send_message(message.chat.id, text)

bot.polling()