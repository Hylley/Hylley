from PIL import Image, ImageDraw, ImageFilter, ImageFont
from textwrap import TextWrapper
from config import *

IMAGE_SLOTS_DISTANCE = 170
IMAGE_SLOTS_SIZE = (147, 147)
IMAGE_SLOT_MARGIN = (65, 75)
IMAGE_INPUT_POSITION  = (IMAGE_SLOT_MARGIN[0], 1375)
IMAGE_DESCRIPTION_WRAP_SIZE = 55
IMAGE_DESCRIPTION_POSITION = (IMAGE_SLOT_MARGIN[0], 995)
IMAGE_TEXT_OFFSET = (0, -10)
WIN_IMAGE_SCORE_POSITION = (158, 1108)

path = 'src\\'


def winScreen(history, guess, description, word, best, overlay = f'{path}overlays\win_screen.png'):
	bottom = generateImage(history, guess, description, word)
	overlay = Image.open(overlay)
	attempts = 0

	if history:
		attempts = len(history)

	score = f"""
Word: {word.upper()}
Score: {MAX_ATTEMPTS - attempts}
Best: {0}
"""

	bottom.paste(overlay, (0, 0), mask=overlay)

	font = ImageFont.truetype(f'{path}fonts\\alliance-n1-light.otf', 70)
	ImageDraw.Draw(bottom).text(WIN_IMAGE_SCORE_POSITION, score, (255, 255, 255), font=font)

	return bottom


def gameOver(history, guess, description, word, best):
	return winScreen(history, guess, description, word, best, f'{path}overlays\game_over_screen.png')


def generateImage(history, guess, description, word):
	canvas = Image.open(f'{path}slots\\canvas.png')

	emptySlot = Image.open(f'{path}slots\\empty.png').resize(IMAGE_SLOTS_SIZE)
	fullSlot = Image.open(f'{path}slots\\full.png').resize(IMAGE_SLOTS_SIZE)
	inputSlot = Image.open(f'{path}slots\\empty_input.png').resize(IMAGE_SLOTS_SIZE)
	orangeSlot = Image.open(f'{path}slots\\full_orange.png').resize(IMAGE_SLOTS_SIZE)
	greenSlot = Image.open(f'{path}slots\\full_green.png').resize(IMAGE_SLOTS_SIZE)

	for v in range(5):
		for h in range(5):
			position = (h * IMAGE_SLOTS_DISTANCE + IMAGE_SLOT_MARGIN[0], v * IMAGE_SLOTS_DISTANCE + IMAGE_SLOT_MARGIN[1])

			if v > len(history) - 1:
				canvas.paste(emptySlot, position, mask=emptySlot)
			else:
				print(h, history[v], word)
				if history[v][h] == word[h]:
					canvas.paste(greenSlot, position)
				elif history[v][h] in word:
					canvas.paste(orangeSlot, position)
				else:
					canvas.paste(fullSlot, position)

				font = ImageFont.truetype(f'{path}fonts\\alliance-n1-light.otf', 130)
				ImageDraw.Draw(canvas).text((position[0] + IMAGE_SLOTS_SIZE[0]//2 + IMAGE_TEXT_OFFSET[0], position[1] + IMAGE_SLOTS_SIZE[1]//2 + IMAGE_TEXT_OFFSET[1]), history[v][h].upper(), (255, 255, 255), font=font, anchor='mm')


	for h in range(5):
		position = (h * IMAGE_SLOTS_DISTANCE + IMAGE_INPUT_POSITION[0], IMAGE_INPUT_POSITION[1])
		canvas.paste(inputSlot, position, mask=inputSlot)

		if len(guess) > h:
			font = ImageFont.truetype(f'{path}fonts\\alliance-n1-light.otf', 130)
			ImageDraw.Draw(canvas).text((position[0] + IMAGE_SLOTS_SIZE[0]//2 + IMAGE_TEXT_OFFSET[0], position[1] + IMAGE_SLOTS_SIZE[1]//2 + IMAGE_TEXT_OFFSET[1]), guess[h].upper(), (255, 255, 255), font=font, anchor='mm')


	text = '\n'.join(TextWrapper(width=IMAGE_DESCRIPTION_WRAP_SIZE).wrap(text='\t'+description))
	font = ImageFont.truetype(f'{path}fonts\\blimone-regular.ttf', 45)
	ImageDraw.Draw(canvas).text(IMAGE_DESCRIPTION_POSITION, text, (255, 255, 255), font=font)

	return canvas
