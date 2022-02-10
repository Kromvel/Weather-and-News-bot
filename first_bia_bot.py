from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, MessageFilter, UpdateFilter, ConversationHandler
from Modules import tokens as tk
from Modules import owmapi as owm
from Modules import guardian_api as news_api
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING = 0
WEATHER = 1
WEATHER_CITY = 2
NEWS = 1

reply_keyboard = [[
            InlineKeyboardButton("Узнать погоду", callback_data='weather'),
            InlineKeyboardButton("Узнать последние новости", callback_data='news')
           ]]
markup = InlineKeyboardMarkup(reply_keyboard)
     


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Выберите, пожалуйста, опцию:', reply_markup=markup)
    return CHOOSING

def echo(update: Update, context: CallbackContext):
    #print(update.message)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Нераспознанное сообщение. Выберите /start')
    return ConversationHandler.END

def weather (update: Update, context: CallbackContext):
    query = update.callback_query
    #print(query.message)
    query_option = query.message.reply_markup['inline_keyboard'][0][0]['text']
    #print(update.callback_query.message.text)
    query.edit_message_text(text=f"Выбрана опция: {query_option}")
    context.bot.send_message(chat_id=update.effective_chat.id, text='Укажите город', reply_markup = ForceReply(force_reply=True, selective=False, input_field_placeholder='Введите название'))

    return WEATHER_CITY

def news (update: Update, context: CallbackContext):
    query = update.callback_query
    query_option = query.message.reply_markup['inline_keyboard'][0][1]['text']
    query.edit_message_text(text=f"Выбрана опция: {query_option}")
    result = news_api.parsing_guardian_news()
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, parse_mode='HTML', reply_markup=markup)
    return CHOOSING
    
def city(update: Update, context: CallbackContext):
    #print(update.message.reply_to_message.text)
    city = update.message.text
    #print(update.message.text)
    result = owm.get_weather(city)
    #print(val)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=markup)
    return CHOOSING

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Отправленная команда не распознана. Пропишите /start")

def main() -> None:
    try:
        updater = Updater(token=tk.BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        start_handler = CommandHandler('start', start)
        unknown_handler = MessageHandler(Filters.command, unknown)
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        city_handler = MessageHandler(Filters.text, city)
        button_weather_handler = CallbackQueryHandler(weather, pattern='weather')
        button_news_handler = CallbackQueryHandler(news, pattern='news')
        '''
        dispatcher.add_handler(start_handler)
        
        
        dispatcher.add_handler(button_weather_handler)
        dispatcher.add_handler(button_news_handler)
        dispatcher.add_handler(city_handler)
        '''
        
        
        conv_handler = ConversationHandler(
            per_message=False,
            entry_points=[start_handler],
            states={
                CHOOSING: [button_weather_handler, button_news_handler],
                WEATHER: [button_weather_handler],
                WEATHER_CITY: [city_handler]
               
            },
            fallbacks=[echo_handler]
        )
       
        
        dispatcher.add_handler(conv_handler)
        dispatcher.add_handler(echo_handler)
        dispatcher.add_handler(unknown_handler)
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()