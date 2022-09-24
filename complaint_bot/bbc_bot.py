import telebot 
import sqlite3 


bot = telebot.TeleBot("token")

language = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
language.row('O\'zbek tili 🇺🇿', 'Русский язык 🇷🇺')

back_uz = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
back_uz.row('Orqaga ↩️')

back_ru = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
back_ru.row('Назад ↩️')

remove_markup = telebot.types.ReplyKeyboardRemove()

send_ru = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
send_ru.row('Отправка данных 📨')

send_uz = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)
send_uz.row('Ma\'lumotlarni jo\'natish  📨')

def send_regions(lang): 
	regions_uz = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
	uzb_regions = ['Toshkent', 'Andijon', 'Buxoro', 'Farg\'ona', 'Jizzax', 
	'Xorazm', 'Namangan', 'Navoiy', 'Qashqadaryo', 'Samarqand', 'Sirdaryo', 'Surxondaryo',
	'Qoraqalpog\'iston Respublikasi']
	regions_uz.add(*uzb_regions)

	regions_ru = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
	rus_regions = ['Ташкент', 'Андижан', 'Бухарa', 'Ферганa', 'Джизак', 'Хорезм', 'Наманган', 
	'Навоий', 'Кашкадаря', 'Самарканд', 'Сырдаря', 'Сурхандаря', 'Республика Каракалпакстан']
	regions_ru.add(*rus_regions)

	return regions_uz if lang == 'O\'zbek tili 🇺🇿' else regions_ru


def write_info(message): 
	conn = sqlite3.connect("bbc_db.db")
	user = message.from_user.id 
	user_name = message.from_user.username
	query = "INSERT INTO user_step (user_id, user_name, step) VALUES ('{user_id}', '{name}', '{step}');".format(user_id=user, name=user_name, step='lang')
	conn.execute(query)
	conn.commit()
	conn.close()


def get_step(user): 
	conn = sqlite3.connect("bbc_db.db") 
	query = "SELECT step FROM user_step WHERE user_id = '{user_id}';".format(user_id=user) 
	cursor = conn.execute(query)
	for row in cursor: 
		step = row[0] 

	conn.close()
	return step  


def get_lang(user): 
	conn = sqlite3.connect("bbc_db.db") 
	query = "SELECT language FROM user_step WHERE user_id = '{user_id}';".format(user_id=user) 
	cursor = conn.execute(query)
	for row in cursor: 
		lang = row[0] 

	conn.close()
	return lang  


def set_step(user, new_step): 
	conn = sqlite3.connect("bbc_db.db")  
	query = "UPDATE user_step SET step = '{step}' WHERE user_id = {user_id};".format(step=new_step, user_id=user) 
	conn.execute(query)
	conn.commit()
	conn.close() 


def set_lang(user, language): 
	print (language)
	conn = sqlite3.connect("bbc_db.db")
	language = 'uzbekcha' if language == 'O\'zbek tili 🇺🇿' else 'ruscha'
	print (language)
	query = "UPDATE user_step SET language = '{lang}' WHERE user_id = {user_id};".format(lang=language, user_id=user)
	conn.execute(query)
	conn.commit()
	conn.close() 


def set_region(user, region):
	conn = sqlite3.connect("bbc_db.db")  
	query = "UPDATE user_step SET region = '{reg}' WHERE user_id = {user_id};".format(reg=region, user_id=user) 
	conn.execute(query)
	conn.commit()
	conn.close()

def set_complain(user, comp):
	conn = sqlite3.connect("bbc_db.db")  
	query = "UPDATE user_step SET complain = \"{compl}\" WHERE user_id = {user_id};".format(compl=comp, user_id=user) 
	conn.execute(query)
	conn.commit()
	conn.close()


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAMQXxX5kZbXZ6xrXBldDWpMJ9q3-88AAh6tMRsJ0bFI4bDUfFXdm4WlaeiSLgADAQADAgADeAADMQcEAAEaBA')
	bot.send_message(message.chat.id, "Xush kelibsiz BBC NEWS rasmiy botiga!")
	write_info(message) # create user in db 
	bot.send_message(message.chat.id, "Tilni tanlang: ", reply_markup = language) 


@bot.message_handler(content_types=['text'])
def send_text(message):
	print (get_step(message.from_user.id))
	bot.forward_message("-1001464294052", message.chat.id, message.message_id)
	if get_step(message.from_user.id) == 'lang':
		set_lang(message.from_user.id, message.text) 
		set_step(message.from_user.id, 'reg')
		if message.text == 'O\'zbek tili 🇺🇿': 
			bot.send_message(message.chat.id, 'Viloyatingizni tanlang: ', reply_markup=send_regions(message.text))
		elif message.text == 'Русский язык 🇷🇺': 
			bot.send_message(message.chat.id, 'Выберите свой регион: ', reply_markup=send_regions(message.text))

	elif get_step(message.from_user.id) == 'reg':
		set_region(message.from_user.id, message.text)

		print(get_lang(message.from_user.id))
		if get_lang(message.from_user.id) == 'uzbekcha':
			bot.send_message(message.chat.id, 'Shikoyatingizni keriting (qo\'shimcha dalil sifatida media material yuborishing mumkin): ', reply_markup=remove_markup) 
		else: 
			bot.send_message(message.chat.id, 'Введите вашу жалобу (Вы можете ввести материал СМИ в качестве доказательства): ', reply_markup=remove_markup)

		set_step(message.from_user.id, 'additional')

	elif message.text in ["Отправка данных 📨", "Ma\'lumotlarni jo\'natish  📨"]:
		set_complain(message.from_user.id, message.text)
		keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

		if get_lang(message.from_user.id) == 'uzbekcha':
			reg_button = telebot.types.KeyboardButton(text="Raqamni Ulashish 📞", request_contact=True)
			keyboard.add(reg_button)
			bot.send_message(message.chat.id, 
									"Sizning raqamingiz: ", 
									reply_markup=keyboard)

		else: 
			reg_button = telebot.types.KeyboardButton(text="Поделиться номером 📞", request_contact=True)
			keyboard.add(reg_button)
			bot.send_message(message.chat.id, 
									"Baш номер: ", 
									reply_markup=keyboard)

	elif get_step(message.from_user.id) == 'additional':
		if get_lang(message.from_user.id) == 'uzbekcha':
			bot.send_message(message.chat.id, 'Qo\'shimcha ma\'lumot yuborish: ', reply_markup=send_uz) 
		else: 
			bot.send_message(message.chat.id, 'Добавление дополнительных данных: ', reply_markup=send_ru)
			
		

	
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
	print(message)

@bot.message_handler(content_types=['contact'])
def handle_docs_photo(message):
	if get_lang(message.from_user.id) == 'uzbekcha':
		bot.send_message(message.chat.id, "Rahmat! Biz ma'lumotlarni ko'rib chiqib siz bilan tez orada bog'lanamiz!")
	else: 
		bot.send_message(message.chat.id, "Спасибо! Мы скоро с вами свяжемся!") 

	bot.forward_message("-1001464294052", message.chat.id, message.message_id)  

	#bot.send_message(message.chat.id, "LOX") 
	#bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMkXvy6bsrOcJ0QGfGkFh6Z3HTwzFsAAjoKAAJuMtgAAS0_oAM8bkDrGgQ')

bot.polling()
