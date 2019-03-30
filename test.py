import config

import pymysql.cursors
import telebot

connection = pymysql.connect(host='localhost',
							 user='root',
							 password='1133',
							 db='tododb',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def record_in_db(message):
	with connection.cursor() as cursor:
		sql = "INSERT INTO user (user_id,username) VALUES (%s, %s)"
		cursor.execute(sql, (str(message.chat.id), str(message.chat.username)))
		connection.commit()
		print('user create', message.chat.id)
		print('user not create or alredy exist')
		sql = "INSERT INTO quests (messages, done) VALUES (%s, %s)"
		cursor.execute(sql, (str(message.text), 0))
		connection.commit()
		print('message create', str(message.text))


@bot.message_handler(content_types=['List'])
def send_helps():
	helps = []
	with connection.cursor() as cursor:
		for i in range(1, 100):
			sql = "SELECT messages FROM quests WHERE id=%s AND done=%s"
			try:
				cursor.execute(sql, (i, 0))
				result = cursor.fetchone()
				if result.get('messages') != '' and result.get('messages') not in helps:
					helps.append(result.get('messages'))
			except:
				pass
	bot.send_message('Текущие задания: {}').format(helps)

if __name__ == '__main__':
	bot.polling(none_stop=True)