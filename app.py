from flask import Flask, request, redirect, url_for, make_response, send_file, send_from_directory
from waitress import serve
from time import sleep
from io import BytesIO
import wordle
import os


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def add_header(response):
		response.cache_control.no_store = True
		response.cache_control.max_age = 0
		response.cache_control.no_cache = True
		print('v')
		return response


@app.route('/', methods=['GET'])
def index():
	"""
		// Authentication

			Each browser will have an individual (and theoreticaly) unique
		ID, wich will also act like a "login" protocol to access that
		specific "player" data.
			The follow code initialy checks at the brower's cookies for
		that mention ID. If it finds, means that the player already has started
		a game. If not, then the program will generate a new one.

		// Gaming!
	"""

	letter = request.args.get('letter')

	if letter is None:
		return 'Good morning, sir!'

	if letter != '' and not letter.isalpha() or len(letter) > 1:
		return ERROR_MESSAGE

	# Authentication
	if not request.cookies.get('userID'):
		userKey = wordle.registerSession()

		resp = make_response(redirect(f'/?userID={userKey}&letter={letter}'))
		resp.set_cookie('userID', str(userKey), secure=True, samesite=None)
		resp.set_cookie('letter', str(letter), secure=True, samesite=None)

		return resp

	userId = request.cookies.get('userID')

	# Gaming!
	response = wordle.game(letter, userId)

	#img_io = BytesIO()
	#response.save(fim_io, 'PNG', quality=90)
	#img_io.seek(0)

	#return send_file(img_io, mimetype='image/png')

	response.save(f'static/image.png', 'PNG', quality=20)
	return redirect('https://github.com/Hylley')


@app.route('/backspace')
def backspace():
	userId = request.cookies.get('userID')

	if not userId:
		return ERROR_MESSAGE

	if wordle.backspace(userId):
		return redirect('/?letter=')


@app.route('/image')
def image():
	return send_from_directory('static', f'image.png')


serve(app, host="0.0.0.0", port=81)
