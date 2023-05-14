from django.core.management.base import BaseCommand
from django.conf import settings

from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from apps.debts.models import Transaction
# from apps.users.models import User


bot = TeleBot(settings.TOKEN, threaded=False)


class Command(BaseCommand):
    help = 'MyCash'

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(
            message,
            f'{message.chat.id}-{"Привет! Я твой тестовый бот."}'
        )

    @bot.message_handler(commands=['my_debts'])
    def my_debts(message):
        # Создаем объект клавиатуры и задаем ее вид
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(KeyboardButton('Назад'))

        # Отправляем сообщение с клавиатурой
        bot.send_message(
            chat_id=message.chat.id,
            text='Выберите долг',
            reply_markup=keyboard,
        )

        # Отправляем список всех долгов
        for debt in Transaction.objects.all():
            bot.send_message(
                chat_id=message.chat.id,
                text=f'{debt.contact}-{debt.amount}',
            )

    @bot.message_handler(func=lambda message: message.text == 'Назад')
    def back(message):
        # Удаляем клавиатуру и отправляем сообщение
        keyboard = ReplyKeyboardRemove()
        bot.send_message(
            chat_id=message.chat.id,
            text='Вы вернулись назад',
            reply_markup=keyboard,
        )

    @bot.message_handler(commands=['help'])
    def help(message):
        commands_list = [
            '/start - Начать работу',
            '/help - Справка',
            '/my_debts - Мои долги'
        ]
        bot.send_message(
            message.chat.id,
            'Список доступных команд:\n{}'.format('\n'.join(commands_list))
        )
