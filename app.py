from flask import Flask, request, redirect, url_for, make_response, send_file
from io import BytesIO
import wordle


app = Flask(__name__)


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

	if letter != '' and not letter.isalpha() or len(letter) > 1:
		return ERROR_MESSAGE

	# Authentication
	if not request.cookies.get('userID'):
		userKey = registerSession()

		resp = make_response(redirect(f'/?userID={userKey}&letter={letter}'))
		resp.set_cookie('userID', str(userKey))
		resp.set_cookie('letter', str(letter))

		return resp

	userId = request.cookies.get('userID')

	# Gaming!
	response = wordle.game(letter, userId)

	img_io = BytesIO()
	response.save(img_io, 'PNG', quality=96)
	img_io.seek(0)
	return send_file(img_io, mimetype='image/png')


@app.route('/backspace')
def backspace():
	userId = request.cookies.get('userID')

	if not userId:
		return ERROR_MESSAGE

	if wordle.backspace(userId):
		return redirect('/?letter=')
