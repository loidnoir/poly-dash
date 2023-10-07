import logging
import os

from dotenv import load_dotenv
from peewee import *
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()
token = os.environ.get('TOKEN')

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db
        table_name = 'users'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    print('Running the bot!')
    app = Application.builder().token(token).build()
    from commands.menu_command import menu_command
    from commands.start_command import start_button_response, start_command
    from user import User
    db.connect()
    db.create_tables([User])
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('menu', menu_command))
    app.add_handler(MessageHandler(filters.TEXT, start_button_response))
    app.run_polling(allowed_updates=Update.ALL_TYPES)