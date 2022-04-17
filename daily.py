import botfile
import database
from datetime import datetime, date, timedelta
import creds
import telebot


def ban_user(user_id):
    botfile.bot.ban_chat_member(creds.chat_id, user_id)

def daily_spam(user_id):
    date_end = database.check_period(user_id)
    if date_end-timedelta(days=7) == date.today():
        botfile.bot.send_message(user_id, 'Уважаемый пользователь! Через 7 дней у вас заканчивается подписка на канал' 
                                   ' *«ПСИХОЛОГИЯ на 1-2 с Галиной Рубцовой»*. Чтобы не потерять к нему доступ - приобретите' 
                                   ' абонемент по удобному тарифу.', parse_mode='Markdown')
    elif date_end-timedelta(days=3) == date.today():
        botfile.bot.send_message(user_id, 'Уважаемый пользователь! Через 3 дня у вас заканчивается подписка на канал'
                                  ' *«ПСИХОЛОГИЯ на 1-2 с Галиной Рубцовой»*. Чтобы не потерять к нему доступ - приобретите'
                                  ' абонемент по удобному тарифу.', parse_mode='Markdown')
    elif date_end-timedelta(days=1) == date.today():
        botfile.bot.send_message(user_id, 'Уважаемый пользователь! Через один день у вас заканчивается подписка на канал'
                                  ' *«ПСИХОЛОГИЯ на 𝟏-𝟐 с Галиной Рубцовой»*. Чтобы не потерять к нему доступ - приобретите'
                                  ' абонемент по удобному тарифу.', parse_mode='Markdown')
    elif date_end == date.today():
        botfile.bot.send_message(user_id, 'Уважаемый пользователь! Сегодня у вас заканчивается подписка на канал'
                                  ' *«ПСИХОЛОГИЯ на 𝟏-𝟐 с Галиной Рубцовой»*. Чтобы не потерять к нему доступ - приобретите'
                                  ' абонемент по удобному тарифу.', parse_mode='Markdown')



def daily():
    for users in database.daily_check():
        user_id = users[0]
        date_end = datetime.strptime(users[1],"%Y-%m-%d").date()
        if date_end < date.today():
            ban_user(user_id)
            database.delete_from_table(user_id)
            try:
                botfile.bot.send_message(user_id,"Подписка на канал *«ПСИХОЛОГИЯ на 1-2 с Галиной Рубцовой»* закончилась."
                                             " Что-бы снова получить доступ к каналу - приобретите абонемент.", parse_mode="Markdown")
            except telebot.apihelper.ApiTelegramException:
                botfile.bot.send_message(1307020973,'Выгнал сегодня: ' + str(user_id) + ' ' + str(date_end))
        else:
            try:
                daily_spam(user_id)
            except telebot.apihelper.ApiTelegramException:
                botfile.bot.send_message(1307020973,'Те, до кого не достучался: ' + str(user_id) +' '+ str(date_end))


daily()