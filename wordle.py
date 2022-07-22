from random import choice
from requests import get
from uuid import uuid4
import image_handling
from config import *
import sqlite3


def randomWord():
	return choice(list(WORDS))


def data(userID):
	con = sqlite3.connect('database.db')
	cur = con.cursor()

	data = cur.execute('SELECT * FROM users WHERE id = ?', [userID]).fetchone()

	cur.close()
	con.close()

	return data


def registerSession():
	key = uuid4()

	con = sqlite3.connect('database.db')
	cur = con.cursor()

	cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, 0)', [str(key), randomWord(), '', ''])
	con.commit()

	cur.close()
	con.close()

	return key


def reset(id):
	con = sqlite3.connect('database.db')
	cur = con.cursor()

	cur.execute('UPDATE users SET word = ?, attempts = "", current_guess = "" WHERE id = ?', [randomWord(), id])

	con.commit()
	cur.close()
	con.close()


def backspace(userId):
	con = sqlite3.connect('database.db')
	cur = con.cursor()

	guess = cur.execute('SELECT current_guess FROM users WHERE id = ?', [userId]).fetchone()[0]

	if guess:
		cur.execute('UPDATE users SET current_guess = ? WHERE id = ?', [guess[:-1], userId])

	con.commit()
	cur.close()
	con.close()

	return True


def game(letter, userId):
	win = False
	id, word, history, guess, bestScore = data(userId)
	description = WORDS[word]

	con = sqlite3.connect('database.db')
	cur = con.cursor()

	guess = guess.lower() + letter.lower()
	cur.execute('UPDATE users SET current_guess = ? WHERE id = ?', [guess, id])

	if len(guess) >= LETTERS:
		response = get(f'https://api.dicionario-aberto.net/word/{guess}')
		cur.execute('UPDATE users SET current_guess = ? WHERE id = ?', ['', id])

		if response != []:
			history = history + f' {guess}'
			cur.execute('UPDATE users SET attempts = ? WHERE id = ?', [history, id])
			if guess == word:
				win = True
			guess = ''

	con.commit()
	cur.close()
	con.close()

	if not win and len(history.split()) + 1 > MAX_ATTEMPTS:
		reset(id)
		return image_handling.gameOver(history.split(), guess, description, word, bestScore)
	elif not win:
		return image_handling.generateImage(history.split(), guess, description, word)

	reset(id)
	return image_handling.winScreen(history.split(), guess, description, word, bestScore)
