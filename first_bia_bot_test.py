from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, MessageFilter, UpdateFilter, ConversationHandler
from Modules import tokens as tk
from Modules import owmapi as owm
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

WEATHER_CITY = 0
NEWS = 0

reply_keyboard = [[
            InlineKeyboardButton("Узнать погоду", callback_data='weather'),
            InlineKeyboardButton("Узнать новость", callback_data='news'),]]
markup = InlineKeyboardMarkup(reply_keyboard)

class FilterCityMessageReply(MessageFilter):
    def filter(self, message):
            return 'Укажите город' in message.reply_to_message.text

        


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Выберите, пожалуйста, опцию:', reply_markup=markup)
    

def echo(update: Update, context: CallbackContext):
    
    context.bot.send_message(chat_id=update.effective_chat.id, text='Выберите /start')
    return ConversationHandler.END

def weather (update: Update, context: CallbackContext):
    query = update.callback_query
    #print(query.message)
    query_option = query.message.reply_markup['inline_keyboard'][0][0]['text']
    query.answer()
    #print(update.callback_query.message.text)
    query.edit_message_text(text=f"Выбрана опция: {query_option}")
    context.bot.send_message(chat_id=update.effective_chat.id, text='Укажите город', reply_markup = ForceReply(force_reply=True, selective=False, input_field_placeholder='Введите название'))
    return WEATHER_CITY

def news (update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")
    context.bot.send_message(chat_id=update.effective_chat.id, text='News', reply_markup=markup)
    return NEWS
    
def city(update: Update, context: CallbackContext):
    #print(update.message.reply_to_message.text)
    #print(update.message.text)
    #owm.get_weather()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Cool')
    return ConversationHandler.END

def main() -> None:
    try:
        updater = Updater(token=tk.BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        start_handler = CommandHandler('start', start)
        
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        city_handler = MessageHandler(FilterCityMessageReply('Укажите город'), city)
        button_weather_handler = CallbackQueryHandler(weather, pattern='weather')
        button_news_handler = CallbackQueryHandler(news, pattern='news')
       
        dispatcher.add_handler(start_handler)
        '''
        dispatcher.add_handler(echo_handler)
        dispatcher.add_handler(button_weather_handler)
        dispatcher.add_handler(button_news_handler)
        dispatcher.add_handler(city_handler)
        '''
        
        conv_weather_handler = ConversationHandler(
            per_message=False,
            entry_points=[button_weather_handler],
            states={
                WEATHER_CITY: [city_handler]
               
            },
            fallbacks=[echo_handler]
        )
        conv_news_handler = ConversationHandler(
            per_message=False,
            entry_points=[button_news_handler],
            states={
               
                NEWS: [button_news_handler]
            },
            fallbacks=[echo_handler]
        )
        dispatcher.add_handler(conv_weather_handler)
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()