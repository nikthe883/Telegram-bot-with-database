# Telegram-bot-with-database
This is a bot for sending messeges in Telegram with database administration for forex signals.


Console based program. With it you can make a couple of things:

Add users to database - when adding new users you can choose the subscription, when the subscription ends. It is important to know their Telegram ID
You can administer the data base - detele users, change their subsciptions, exporting the data base to excel.
The app automatically checks if the user subscription is over acnd changes the user status.
The app warns you when there are users with ending subscuptions.
You can choose to whom to send the message - paid users, upaid users, to two telegram groups or to all.
And many more...
However to send a messege to somebody. He/she needs to initialize conversation with the bot.

There is a predefined message which looks like this:

![Capture4](https://user-images.githubusercontent.com/82037390/170830630-1cbe36ab-842c-4d57-a484-9d5e011588a1.PNG)

However you can even write your own message.

In dependencies there are a couple of things you need to add:

TOKEN = "This is the bots token"

PAID_TELEGRAM_GROUP_ID = ""

UNPAID_TELEGRAM_GROUP_ID = ""

ADMIN_ID = "Your Telegram ID"

Here are some pictures of the program:

Main menu:

![Capture](https://user-images.githubusercontent.com/82037390/170830576-2a1dd6f2-77ba-4a24-ab8e-fd57115ae0b7.PNG)

Choose to which Telegram users to send messsage:

![Capture1](https://user-images.githubusercontent.com/82037390/170830611-2fbb7846-8f35-4538-91ff-afa97743d47d.PNG)

Adding a new user:

![Capture3](https://user-images.githubusercontent.com/82037390/170830627-717555b0-e727-4a3f-9732-481843079f91.PNG)

The app warns you that the paid subscription to user is ending:

![Capture5](https://user-images.githubusercontent.com/82037390/170830668-919cb131-47b6-4a53-b246-1705ecec3fcd.PNG)

Administration of users:

![Capture6](https://user-images.githubusercontent.com/82037390/170830685-3ddb4f6e-a3c6-4502-a4f8-7bed50a40ea5.PNG)
