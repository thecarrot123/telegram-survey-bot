from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import main
import os

telegram_bot_token = os.getenv("BOT_TOKEN")

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

def startCommand(update, context):
    chat_id = update.message.chat.id
    username = update.message.chat.username
    reply = main.start(chat_id,username)
    context.bot.send_message(chat_id=chat_id, text=reply)

def askCommand(update, context):
    chat_id = update.message.chat.id
    message = update.message.text
    reply = main.ask(chat_id, message)
    update.message.reply_text(reply)

def helpCommand(update, context):
    reply = """ 
    To create a question use </ask "Question">. This will return a message with a token.

    To answer a question just send the question token you want to answer. This will return a message with the question.
Send your answer in the next message. Only one message is saved.To edit your answer just resend your token."""
    update.message.reply_text(reply) 

def messageHandlerCommand(update, context):
    chat_id = update.message.chat.id
    message = update.message.text
    reply = main.messageHandler(chat_id,message)
    update.message.reply_text(reply)

def collectAnswersCommand(update, context):
    chat_id = update.message.chat.id
    message = update.message.text.split(' ',1)
    reply = main.collectAnswers(chat_id, message)
    update.message.reply_text(reply)


dispatcher.add_handler(CommandHandler("start", startCommand))
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("ask", askCommand))
dispatcher.add_handler(CommandHandler("collect", collectAnswersCommand)) # todo

#commands = [
#    {"command":"start","description":"start bot"},
#    {"command":"answer","description":"give token to answer question"},]


dispatcher.add_handler(MessageHandler(Filters.text, messageHandlerCommand))
if main.env_config == "flask_config.TestConfig":
    main.runTests()

print("Starting bot:")
updater.start_polling()