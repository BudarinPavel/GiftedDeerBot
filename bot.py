import telebot
import config
import random
import datetime

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

gifts = ['Новогодний плед с рукавами', '3D-светильники на стену', 'Снежный бластер', 
		'Корзинка фруктов', 'Шапка ушанка', 'многоразовые кубики льда для напитков', 
		'Термокружка', 'Power bank камень', '3D-ручка', 
		'фитнес-трекер', 'Кружка-мешалка', 'Билеты на каток', 
		'Меховые наушники', 'Скетчбук', 'Подписка на стриминговые сервисы', 
		'Уточка для ванны', 'Небесный фонарик "Новогодний"', 'Гирлядна', 
		'Настольный биокамин', 'Плед фото-коллаж', 'Фейерверки']

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('static/hi.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)

	# keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("🎁Получить подарок!🎁")

	markup.add(item1)

	now = datetime.datetime.today()
	NY = datetime.datetime(2021,1,1)
	d = NY-now
	mm, ss = divmod(d.seconds, 60)
	hh, mm = divmod(mm, 60)

	bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b> \nОлень-бот, который подкинет идеи новогодних подарков для друзей и родных.\n👇Скорее жми кнопку ниже👇\nВедь до нового года осталось всего {2} дней {3} часа {4} мин.".format(message.from_user, bot.get_me(), d.days, hh, mm), 
		parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def choosing_gift(message):
	if message.chat.type == 'private':
		if message.text == '🎁Получить подарок!🎁':

			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton('Класс! 👍', callback_data='good')
			item2 = types.InlineKeyboardButton('Не очень. 👎', callback_data='bad')

			markup.add(item1, item2)

			bot.send_message(message.chat.id, 'Лови идею новогоднего подарка! \n{}'.format(gifts[random.randint(0, len(gifts)-1)]),
				reply_markup=markup)
		else:
			bot.send_message(message.chat.id, 'Скорее жми кнопку внизу, чтобы узнать идею классного подарка')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Рад был помочь тебе!')
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Что ж, попробуй посмотреть другие идеи.\nКнопка с подарками все еще на месте')

			# remove inline buttons
			#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Лови идею новогоднего подарка!", reply_markup=None)

	except Exception as e:
		print(repr(e))

# RUN
bot.polling(none_stop=True)