import telebot
from telebot import types
from telebot.types import LabeledPrice
import creds
import database



token = creds.token
bot = telebot.TeleBot(token)
pay_token = creds.pay_token

markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """

def main():
    def add_user(user_id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('ссылка на канал', url=creds.chat_link)
        markup.add(btn)
        bot.send_message(user_id,'Для доступа нажмите: ', reply_markup=markup)

    def unbun_user(user_id):
        bot.unban_chat_member(creds.chat_id, user_id)

    @bot.message_handler(commands=['start'])
    def start_func(message):
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('ЕЖЕМЕСЯЧНЫЙ АБОНЕМЕНТ')
        btn2 = types.KeyboardButton('АБОНЕМЕНТ ПО ПАКЕТАМ')
        markup.add(btn1,btn2)
        photo = open('images/cotton.jpg', 'rb')
        bot.send_photo(user_id, photo)
        bot.send_message(user_id,
                         'Добро пожаловать в платежный бот канала *«ПСИХОЛОГИЯ на 𝟏-𝟐 с Галиной Рубцовой»*! Для того что бы получить доступ'
                         ' к основному контенту - выберите подходящий вам абонемент и произведите оплату.',
                         reply_markup=markup, parse_mode="Markdown")



    @bot.message_handler(content_types=['text'])
    def stage2(message):
        user_id = message.from_user.id
        if(message.text == 'ЕЖЕМЕСЯЧНЫЙ АБОНЕМЕНТ'):
            bot.send_invoice(
                user_id,
                "АБОНЕМЕНТ НА МЕСЯЦ",
                "Абонемент на месяц доступа к каналу «Психология на 1-2 с Галиной Рубцовой»",
                "payload",
                pay_token,
                "RUB",
                prices=[LabeledPrice(label='Руб',
                                     amount=39000)]
            )
        elif(message.text == 'АБОНЕМЕНТ ПО ПАКЕТАМ'):
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('на 3 месяца', callback_data='3')
            btn2 = types.InlineKeyboardButton('на 5 месяцев', callback_data='5')
            btn3 = types.InlineKeyboardButton('на 7 месяцев', callback_data='7')
            btn4 = types.InlineKeyboardButton('на 12 месяцев', callback_data='12')
            markup.add(btn1,btn2,btn3,btn4)
            bot.send_message(user_id,'*Выберите абонемент:* ', reply_markup=markup, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('3'))
    def threemonth(call):
        user_id = call.from_user.id
        bot.send_invoice(
            user_id,
            "АБОНЕМЕНТ НА ТРИ МЕСЯЦА",
            "Абонемент на три месяца доступа к каналу «Психология на 1-2 с Галиной Рубцовой»",
            "payload",
            pay_token,
            "RUB",
            prices=[LabeledPrice(label='Руб',
                                 amount=100000)]
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('5'))
    def fivemonth(call):
        user_id = call.from_user.id
        bot.send_invoice(
            user_id,
            "АБОНЕМЕНТ НА ПЯТЬ МЕСЯЦЕВ",
            "Абонемент на пять месяцев доступа к каналу «Психология на 1-2 с Галиной Рубцовой»",
            "payload",
            pay_token,
            "RUB",
            prices=[LabeledPrice(label='Руб',
                                 amount=170000)]
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('7'))
    def sevenmonth(call):
        user_id = call.from_user.id
        bot.send_invoice(
            user_id,
            "АБОНЕМЕНТ НА СЕМЬ МЕСЯЦЕВ",
            "Абонемент на семь месяцев доступа к каналу «Психология на 1-2 с Галиной Рубцовой»",
            "payload",
            pay_token,
            "RUB",
            prices=[LabeledPrice(label='Руб',
                                 amount=240000)]
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('12'))
    def sevenmonth(call):
        user_id = call.from_user.id
        bot.send_invoice(
            user_id,
            "АБОНЕМЕНТ НА ГОД",
            "Абонемент на двенадцать месяцев доступа к каналу «Психология на 1-2 с Галиной Рубцовой»",
            "payload",
            pay_token,
            "RUB",
            prices=[LabeledPrice(label='Руб',
                                 amount=400000)]
        )

    @bot.pre_checkout_query_handler(func=lambda query: True)
    def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        @bot.message_handler(content_types=['successful_payment'])
        def successfful_payment(message):
            user_id = message.from_user.id
            payment = pre_checkout_query.total_amount
            username = message.from_user.username
            firstname = message.from_user.first_name
            lastname = message.from_user.last_name
            database.open_order(user_id, payment, username, firstname, lastname)
            bot.send_message(user_id, '*Оплата прошла успешно* ', parse_mode="Markdown")
            try:
                unbun_user(user_id)
                add_user(user_id)
            except telebot.apihelper.ApiTelegramException:
                add_user(user_id)
