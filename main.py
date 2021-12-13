import os
import logging
import state_machine

from dotenv import load_dotenv
from telegram import (Update, KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, Filters, MessageHandler, CallbackContext)

load_dotenv()  # грузим и подключаем токен

TELEGRAM_TOKEN = os.getenv('TOKEN')

logging.basicConfig(  # создаем логер
    format='%(asctime)s - %(name)s - %(levelname)n - %(message)%', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = state_machine.CheeseBot()


def start(update: Update, context: CallbackContext):
    bot.start()  # функция запуска бота
    message = 'Добро пожаловать.\nКакую вы хотите пиццу? Большую или маленькую?\n' \
              'Если Вам нужна помощь введите команду /help.'
    update.message.reply_text(message)
    return


def stop(update: Update, context: CallbackContext):
    bot.stop()  # функция остановки работы бота и возвращение в исходное состояние
    message = 'Для заказа введите /start.'
    update.message.reply_text(message)
    return


def help(update: Update, context: CallbackContext):
    bot.help()  # функция вызова подсказки
    message = 'Для начала формирования заказа введите /start, чтобы отменить заказ /stop.\n' \
              'Пока у нас есть только два варината пиццы: большая и маленькая.\n' \
              'А оплату мы принимаем либо наличкой, либо картой.'
    update.message.reply_text(message)
    return


def run(update: Update, context: CallbackContext):  # основная функция, которая изменяет состояние стейт-машины
    text = update.message.text.lower()
    sizes = [
        'большую', 'маленькую', 'большая', 'маленькая'
    ]
    paying = [
        'наличкой', 'картой', 'онлайн', 'наликом', 'курьеру'
    ]
    if bot.state == 'size_choose':
        if text in sizes:
            bot.pay()
            bot.set_size(text)
            message = 'Как вы будете платить?'
            update.message.reply_text(message)
        else:
            update.message.reply_text('К сожалению я вас не понимаю.\n'
                                      'Сейчас мы доставляем большую или маленькую пиццу.\n'
                                      'Выберите из предложенных.')
    elif bot.state == 'payment_method':
        if text in paying:
            bot.confirm()
            bot.set_payment(text)
            message = f'Вы хотите {bot.size} пиццу, оплата - {bot.payment}?'
            update.message.reply_text(message)
        else:
            update.message.reply_text('Пожалуйста, выберите способ оплаты. Сейчас доступно два варианта оплаты:'
                                      'картой или наличкой.')
    elif bot.state == 'confirmation':
        if text == 'да':
            bot.done()
            contact_button = KeyboardButton('Номер', request_contact=True)  # кнопка-запрос номера телефона
            location_button = KeyboardButton('Адрес', request_location=True)  # кнопка-запрос номера геолокации
            my_keyboard = ReplyKeyboardMarkup([[contact_button, location_button]], resize_keyboard=True)
            message = 'Спасибо за заказ.\n' \
                      'Он отправлен на кухню, но для доставки нам нужны Ваши контакты.\n' \
                      'Для еще одного заказа введите /start.'
            update.message.reply_text(message, reply_markup=my_keyboard)
        elif text == 'нет':
            bot.done()
            message = 'Так, видимо Вы еще не определились, давайте попробуем заново.\n' \
                      'Введите команду /start'
            update.message.reply_text(message)


def main():  # запускаем бота
    updater = Updater(TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('stop', stop))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text, run))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
