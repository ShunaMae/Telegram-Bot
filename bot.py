import deepl
import telegram 
import requests
import telegram.ext
from telegram.ext.updater import Updater 
from telegram.update import Update


deepl_api = "cea5033b-ca96-6681-fe59-cfc64050d7c5:fx"
tele_api = "6347121518:AAHfRqY2ClL2TVi3RwdcFklTgjr8dWHZ9Jo"
BOT_USERNAME = '@lebab_bot'

bot = telegram.Bot(token = tele_api)

def translate_text(text, target_lang):
    url = f'https://api-free.deepl.com/v2/translate?auth_key={deepl_api}&text={text}&target_lang={target_lang}'
    response = requests.get(url)
    data = response.json()
    translated_text = data['translations'][0]['text']
    return translated_text

# Commands 
def start_command(update, context):
    update.message.reply_text("Welcome to the translation bot! Please type /list to see the list of commands available.")

def what_command(update, context):
    update.message.reply_text("This is a Telegram bot that helps you translate words/sentences into one of the following languages: English(en), Japanese(ja), Chinese(zh), and Spanish(es).")

def lang_command(update, context):
    update.message.reply_text("Please choose the tanget language: en (English), ja(Japanese), es (Spanish), zh(Chinese)")
    context.user_data['waiting_for_target_lang'] = True


def jasmine_command(update, context):
    update.message.reply_text("Jasmine is my beautiful soon-to-be wife. She is the motivation of my life, and I cannot thank her enough for how much she has done for me so far. I love her very much :) ")

def list_command(update, context):
    update.message.reply_text("The availabe commands are \n /start: It will welcome you to this bot. \n /what: It will tell you what this bot can do.\n /lang: Used to select the target lauguage \list: show the available commands.")

def handle_message(update, context):
    chat_id = update.message.chat_id
    message = update.message.text


    waiting_for_target_lang = context.user_data.get('waiting_for_target_lang', False)

    if waiting_for_target_lang:
        # The bot is waiting for the target language from the user
        context.user_data['target_lang'] = message
        proper = "a"
        if message == "en":
            proper = "English"
        elif message =="ja":
            proper = "Japanese"
        elif message == "zh":
            proper = "Chinese"
        elif message == "es":
            proper = "Spanish"
        else:
            proper = "unknown"
        context.user_data['waiting_for_target_lang'] = False  # Reset the flag
        update.message.reply_text(f"Target language set to {proper}.")
    else:
        # The bot is not waiting for the target language; it's a regular message
        target_lang = context.user_data.get('target_lang', 'en')  # Default to English

        # Translate the message using the stored target language
        translated_message = translate_text(message, target_lang)

        # Send the translated message back to the user
        context.bot.send_message(chat_id=chat_id, text=translated_message)


updater = telegram.ext.Updater(tele_api, use_context = True)

dp = updater.dispatcher

dp.add_handler(telegram.ext.CommandHandler("start", start_command))
dp.add_handler(telegram.ext.CommandHandler("what", what_command))
dp.add_handler(telegram.ext.CommandHandler("lang", lang_command))
dp.add_handler(telegram.ext.CommandHandler("list", list_command))
dp.add_handler(telegram.ext.CommandHandler("jasmine", jasmine_command))
dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()


