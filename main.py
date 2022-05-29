from telegram import Bot
from telegram.error import BadRequest, Unauthorized
from sqlite3 import OperationalError
from dependencies import *
import sqlite3
from datetime import datetime
import pandas as pd


# connects to DB and gets the time
con = sqlite3.connect("subscription.db")
cur = con.cursor()
today_date = datetime.today().date()


# menu
def menu():
    """Main menu function"""
    # auto checks if there are users with subscription
    # time remaining one day

    check_user_subscription_time()

    auto_change_user_plan()

    # options menu
    option = input("Моля, изберете опция :\n"
                   "1. Добавяне на потребител.\n"
                   "2. Администриране на потребители.\n"
                   "3. Пращане на Телеграм съобщение.\n"
                   "4. Изход.\n"
                   )

    if option == "1":
        helper_option_one()

    elif option == "2":
        helper_option_two()

    elif option == "3":
        helper_option_three()

    elif option == "4":
        exit()

    else:
        print("Моля, изберете валидна опция.\n")


def helper_option_one():
    """Helper function for option one"""
    print("Натиснете 0 ако желаете да се върнете в главното меню\n")

    # takes user input to add to db
    name = input("Въведете името на потребителя.\n")
    if name == "0":
        menu()

    telegram_id = input("Въведете Телеграм ID на потребителя.\n")
    if telegram_id == "0":
        menu()

    subscription = input("Моля въведете платен или неплатен.\n")
    if subscription == "0":
        menu()

    # checks if subscription has valid input
    if subscription == "платен" or subscription == "неплатен":
        if subscription == "платен":
            date_overdue = input("Моля, въведете кога изтича абонамента, във формат : година-месец-ден\n")
            remaining_days = remaining_subscription_days(date_overdue)
            add_user(name, telegram_id, subscription, date_overdue, remaining_days)

        else:
            add_user(name, telegram_id, subscription)
    else:
        print("Грешно въведени данни.\n")

    # asks again the user if wants to continue or go back
    user_decision = input("Натиснете 1 да добавите още един потребител или 0 да се върнете към главното меню.\n")

    if user_decision == "1":
        helper_option_one()

    elif user_decision == "0":
        menu()

    else:
        print("Грешно въведени данни.\n")


def helper_option_two():
    """Helper function for option two"""
    user_input = input("Моля, изберете опция\n"
                       "1. База данни към ексел.\n"
                       "2. Премахване на потребител.\n"
                       "3. Търсене на потребител.\n"
                       "4. Промяна статус потребител.\n"
                       "5. Проверка оставащо време на потребител.\n"
                       "6. Обратно\n"
                       )
    if user_input == "6":
        menu()
    # fool proof
    fool_proof_list = ["1", "2", "3", "4", "5"]

    if user_input in fool_proof_list:
        db_administration(user_input)
    else:
        print("Грешно въведени данни.\n")
        helper_option_two()

    # asks the user if wants to stay
    user_decision = input("Натиснете 1 да останете или 0 да се върнете към главното меню.\n")

    if user_decision == "1":
        helper_option_two()

    elif user_decision == "0":
        menu()

    else:
        print("Грешно въведени данни.\n")


def helper_option_three():
    """Helper function for option three"""
    print("Преди да изпратите индивидуално съобщение,\n"
          "моля проверете дали потребителите са започнали разговор с робота.\n")

    user_input = input("Моля, изберете на кои потребители искате да изпратите сигнал.\n"
                       "1. Индивидуално съобщение до всички платени потребители.\n"
                       "2. Индивидуално съобщение до всички неплатени потребители.\n"
                       "3. Индивидуално съобщение до всички потребители.\n"
                       "4. Съобщение до платена Телеграм група.\n"
                       "5. Съощение до безплатна Телеграм група.\n"
                       "6. Съобщение до двете Телеграм групи.\n"
                       "7. Обратно.\n")

    if user_input == "7":
        menu()

    # fool proof
    fool_proof_list = ["1", "2", "3", "4", "5", "6"]

    if user_input in fool_proof_list:
        select_users(user_input)
    else:
        print("Грешно въведени данни.\n")
        helper_option_three()


def printing_user_helper(row):
    """Helper function for printing information about users."""
    print(f"Име : {row[0]}\n"
          f"Телеграм ID : {row[1]}\n"
          f"Статус : {row[2]}\n"
          f"Платен статус до : {row[3]}\n"
          f"Дата на регистрация : {row[4]}\n"
          f"Оставащи дни до край платен статус : {row[5]}")


def add_user(name, telegram_id, subscription, date_overdue=None, remaining_days=None):
    """Function that adds user to db. Prints the added user """

    cur.execute('''CREATE TABLE IF NOT EXISTS Потребители
            (name text,telegram_id text PRIMARY KEY, subscription text,end_subscription_date timestamp,date_subscription_created timestamp,remaining_days text)''')

    cur.execute('''INSERT OR IGNORE INTO Потребители VALUES
               (?,?,?,?,?,?)''', (name, telegram_id, subscription, date_overdue, today_date, remaining_days))

    con.commit()
    print("Потребителят е успешно добавен!\n")
    # printing the added user
    for row in cur.execute(f'''SELECT * FROM Потребители WHERE telegram_id = "{telegram_id}"'''):
        printing_user_helper(row)


def remaining_subscription_days(date_overdue=None):
    """Checks remaining time for account."""

    remaining_days = datetime.strptime(date_overdue, '%Y-%m-%d').date()
    return str(remaining_days - today_date)


def db_administration(user_input):
    """Function for db administration"""

    if user_input == "1":
        # output the database into excel file
        df = pd.read_sql_query("select * from Потребители", con)
        df.to_excel("Потребители.xlsx", index=False)
        print("Таблицата направена с името Потребители.\n")

    elif user_input == "2":
        # deletes a user
        delete_user = input("Моля, въведете името на потребителя за да го изтриете.\n")
        delete_user_sql = '''DELETE FROM Потребители WHERE name=?'''
        cur.execute(delete_user_sql, (delete_user,))
        con.commit()
        print(f"Потребителя {delete_user} е изтрит !")

    elif user_input == "3":
        # searches for user.
        search_user_name = input("Моля въведете имете на потребителя, който търсите.\n")
        cur.execute(f'''SELECT * FROM Потребители WHERE name = "{search_user_name}"''')
        data = cur.fetchall()
        # checks if user is found or not
        if data is None:
            print("Не е намерен потребител с това име.\n")
        else:
            for row in data:
                printing_user_helper(row)

    elif user_input == "4":
        # changes the status of the user
        user_name_to_update = input("Моля, въведете името на потребителя, на който желаете да промените статуса.\n")
        sql_check_query = f'''SELECT * FROM Потребители WHERE name = "{user_name_to_update}"'''
        cur.execute(sql_check_query)
        data = cur.fetchall()
        # checks if user is found or not
        if data is None:
            print("Не е намерен потребител с това име.\n")
        else:
            # asks the admin what is the status платен or неплатен
            # if the status is changed to платен asks for end date
            # and changes the user information in the database
            # same is for status неплатен
            subscription_status = input("Моля, въведете платен или неплатен.\n")
            if subscription_status == "платен":

                end_subscription = input("Моля, въведете крайна дата за платения потребителски статус във формат : година-месец-ден\n")
                rem_days = remaining_subscription_days(end_subscription)
                sql_update_query = """UPDATE Потребители SET subscription = ?,end_subscription_date = ? ,date_subscription_created = ?,remaining_days = ? WHERE name = ?"""
                cur.execute(sql_update_query, (subscription_status, end_subscription, today_date, rem_days, user_name_to_update,))
                con.commit()

                print("Потребителски статус променен.\n")
                for row in data:
                    printing_user_helper(row)

            elif subscription_status == "неплатен":
                sql_update_query = """UPDATE Потребители SET subscription = ?,end_subscription_date = ?,remaining_days = ? WHERE name = ?"""
                cur.execute(sql_update_query, (subscription_status, None, None, user_name_to_update,))
                con.commit()

                print("Потребителски статус променен.\n")
                for row in data:
                    printing_user_helper(row)

    elif user_input == "5":
        # manual check for user subscription time
        manual_check_user_subscription_time()


def select_users(user_input):
    """A helper function for sending Telegram messages"""
    if user_input == "1":
        paid_user_id = '''SELECT telegram_id FROM Потребители WHERE subscription = "платен"'''
        cur.execute(paid_user_id)
        records = [item[0] for item in cur.fetchall()]
        send_telegram_message(records)

    if user_input == "2":
        paid_user_id = '''SELECT telegram_id FROM Потребители WHERE subscription = "неплатен"'''
        cur.execute(paid_user_id)
        records = [item[0] for item in cur.fetchall()]
        send_telegram_message(records)

    elif user_input == "3":
        paid_user_id = '''SELECT telegram_id FROM Потребители '''
        cur.execute(paid_user_id)
        records = [item[0] for item in cur.fetchall()]
        send_telegram_message(records)

    elif user_input == "4":
        send_telegram_message([PAID_TELEGRAM_GROUP_ID])

    elif user_input == "5":
        send_telegram_message([UNPAID_TELEGRAM_GROUP_ID])

    elif user_input == "6":

        group_id_list = [PAID_TELEGRAM_GROUP_ID, UNPAID_TELEGRAM_GROUP_ID]
        send_telegram_message(group_id_list)


def manual_check_user_subscription_time():
    """Manually checks user subscription time remaining."""
    try:
        user_input = input("Моля, въведете името на потребителя, на който искате да проверите абонамента.\n")

        check_paid_user_time = '''SELECT remaining_days FROM Потребители WHERE name  = ?'''
        cur.execute(check_paid_user_time, (user_input,))
        records = [item[0] for item in cur.fetchall()]
        print(f"На потребител {user_input}, му остават {records} дни до края на абонамента.\n")

        user_decision = input("Натиснете 1 да останете или 0 да се върнете към главното меню.\n")

        if user_decision == "1":
            manual_check_user_subscription_time()

        elif user_decision == "0":
            helper_option_two()

        else:
            print("Грешно въведени данни.\n")

    except OperationalError:
        print("Моля, добавете потребите за да създадете базата данни.\n")


def check_user_subscription_time():
    """Auto checks for users with subscription time 1 day and warns the admin."""
    try:

        days = "1 day, 0:00:00"

        check_paid_user_time = '''SELECT name FROM Потребители WHERE remaining_days  = ?'''
        cur.execute(check_paid_user_time, (days,))
        records = [item[0] for item in cur.fetchall()]
        records = " ".join([item for item in records])

        print(f"!!!!!!!!!!!!!!!!!!!!!!!ВАЖНО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
              f"____________________________________________________________\n"
              f"На тези потребители им изтича платения статус до края на деня!\n"
              f"\n"
              f"{records}\n"
              f"____________________________________________________________\n"
              f"\n")

    except OperationalError:
        print("")


def auto_change_user_plan():
    """Function that changes the user subscription plan
    automatically when the paid subscription expires."""
    try:
        check_paid_user_time = '''SELECT name FROM Потребители WHERE remaining_days  = "0:00:00"'''
        cur.execute(check_paid_user_time, )
        records = [item[0] for item in cur.fetchall()]

        sql_update_query = """UPDATE Потребители SET subscription = "наплатен" ,end_subscription_date = ?,remaining_days = ? WHERE name = ?"""
        for i in records:
            cur.execute(sql_update_query, (None, None, i,))
            con.commit()
    except OperationalError:
        pass

def predefined_message():
    """Helper function for predefined Telegram message"""

    signal_strength_color = ""
    currency = input("Моля, въведете инструмент за търговия.\n")
    stake = input("Моля, въведете вид сигнал - Buy или Sell.\n")

    strength = input("Моля, изберете силата на сигнала:\n"
                     "1.Силен.\n"
                     "2.Нормален.\n"
                     "3.Слаб.\n")
    if strength == "1":
        signal_strength_color = "\U0001F7E2"
    elif strength == "2":
        signal_strength_color = "\U0001F7E2"
    elif strength == "3":
        signal_strength_color = "\U0001F534"
    else:
        print("Моля, изберете валидна опция.\n")

    entry = input("Моля, въведете цена за вход.\n")
    stop_loss = input("Моля, въведете цена за stop loss.\n")
    take_profit = input("Моля, въведете цена за take profit.\n")

    message = f"Trading signal by bot \n" \
              f"Strength : {signal_strength_color}\n" \
              f"---------------------\n" \
              f"Currency : {currency} \n" \
              f"Stake : {stake} \n" \
              f"Entry : {entry}\n" \
              f"SL {stop_loss}" \
              f"TP: {take_profit} \n "
    return message


def send_telegram_message(records):
    """Function for sending Telegram messages."""

    message = ""
    bot = Bot(TOKEN)
    # asks user what kind of message to send
    user_input = input("1. Предварително направено съобщение.\n"
                       "2. Свободно съобщение.\n")

    # predefined message - calls the predefined message function
    if user_input == "1":
        message = predefined_message()

    # free text
    elif user_input == "2":
        message = input("Моля, напишете съобщение.\n")

    # asks user to check the message before sending it to everybody
    check_message = input("Желаете ли да проверите съобщението преди да го изпратите ? \n"
                          "1. Да\n"
                          "2. Не\n")
    # sending the message to admin telegram for proof reading.
    if check_message == "1":
        bot.send_message(ADMIN_ID, text=message)
        print("Съобщението изпратено до админ през Телеграм.\n")

        # asking if the message is approved or not.
        send_message = input("Желаете ли да изпратите съобщението до всички ?\n"
                             "1. Да\n"
                             "2. Не\n")

        # sending the message to selected users
        if send_message == "1":
            send(bot, records, message)

        # not sending the message
        elif send_message == "2":
            menu()

        # fool proof
        else:
            print("Грешно въведени данни.\n")

    # sending message to selected users without proof reading
    elif check_message == "2":
        send(bot, records, message)

    # fool proof
    else:
        print("Грешно въведени данни.\n")


def send(bot, records, message):
    """The function that sends the message to the users"""
    for i in records:
        try:
            # sending message successfully to users
            bot.send_message(i, text=message)
            message_send_user_name = '''SELECT name FROM Потребители WHERE telegram_id = ? '''
            cur.execute(message_send_user_name, (i,))
            message_send_user_name = [item[0] for item in cur.fetchall()]
            print(f"Съобщението се изпрати до следните потребители : {message_send_user_name}")

        except BadRequest:

            # exception when user is not found
            message_not_send_user_name = '''SELECT name FROM Потребители WHERE telegram_id = ? '''
            cur.execute(message_not_send_user_name, (i,))
            message_not_send_user_name = [item[0] for item in cur.fetchall()]
            print(f"Съобщението не се изпрати до следните потребители : {message_not_send_user_name}\n"
                  f"Причина : Грешно Телеграм id\n")

        except Unauthorized:

            # exception when user has not initialize conversation with bot.
            # Only for individual messaging to users.

            message_not_send_user_name = '''SELECT name FROM Потребители WHERE telegram_id = ? '''
            cur.execute(message_not_send_user_name, (i,))
            message_not_send_user_name = [item[0] for item in cur.fetchall()]
            print(f"Съобщението не се изпрати до следните потребители : {message_not_send_user_name}\n"
                  f"Причина : Потребителят не е започнал разговор с робота.\n")


if __name__ == "__main__":
    while True:
        menu()

