from telegram import Bot
from telegram.ext import *
from telegram import Update
from telegram.error import BadRequest, Unauthorized
from dependencies import *
import sqlite3
import logging


class TelegramBot:

    def __init__(self):

        self.updater = Updater(TOKEN, use_context=True)
        self.disp = self.updater.dispatcher

        self.disp.add_handler(CommandHandler("start", self.start))
        self.disp.add_handler(CommandHandler("help", self.help))
        self.disp.add_handler(CommandHandler("id", self.id))

        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, context):
        update.message.reply_text("Здрасти")

    def help(self, update, context):
        update.message.reply_text("""
        Избери някоя от следните команди:
        
        /start -> Добре дошъл.
        /help -> Помощ.
        /id -> Твоето Телеграм ID
        
        """)

    def id(self, bot, update, context):
        chat_id = update.message.chat_id()
        print(chat_id)

class BotSend:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bot = Bot(TOKEN)
        con = sqlite3.connect("subscription.db")
        self.cur = con.cursor()
        logging.basicConfig(filename='telegramboterrors.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')

    def send(self, records, message, both_groups=None):
        for i in records:
            try:
                # sending message successfully to users
                self.bot.send_message(i, text=message)
                if both_groups:
                    print(f"Съобщението се изпрати до групата.")
                else:
                    message_send_user_name = '''SELECT name FROM Потребители WHERE telegram_id = ? '''
                    self.cur.execute(message_send_user_name, (i,))
                    message_send_user_name = [item[0] for item in self.cur.fetchall()]
                    print(f"Съобщението се изпрати до следните потребители : {message_send_user_name}")

            except BadRequest as e:

                # exception when user is not found
                message_not_send_user_name = '''SELECT name FROM Потребители WHERE telegram_id = ? '''
                self.cur.execute(message_not_send_user_name, (i,))
                message_not_send_user_name = [item[0] for item in self.cur.fetchall()]
                print(f"Съобщението не се изпрати до следните потребители : {message_not_send_user_name}\n"
                      f"Причина : Грешно Телеграм id\n")
                self.logger.error(e)

            except Unauthorized:

                # exception when user has not initialize conversation with bot.
                # Only for individual messaging to users.

                message_not_send_user_name = '''SELECT name FROM Потребители WHERE telegram_id = ? '''
                self.cur.execute(message_not_send_user_name, (i,))
                message_not_send_user_name = [item[0] for item in self.cur.fetchall()]
                print(f"Съобщението не се изпрати до следните потребители : {message_not_send_user_name}\n"
                      f"Причина : Потребителят не е започнал разговор с робота.\n")

    def image(self, records, path):
        for i in records:
            self.bot.send_photo(i, photo=open(path, 'rb'))
