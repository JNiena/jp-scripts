import json
import re
import requests
import time
import urllib.request

def request(action, **params):
  return { 'action': action, 'params': params, 'version': 6 }

def invoke(action, **params):
	requestJson = json.dumps(request(action, **params)).encode('utf-8')
	response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))

	if len(response) != 2:
		raise Exception('The response has an unexpected number of fields.')

	if 'error' not in response:
		raise Exception('The response is missing a required error field.')

	if 'result' not in response:
		raise Exception('The response is missing a required result field.')

	if response['error'] is not None:
		raise Exception(response['error'])

	return response['result']

def massif(data):
	return re.findall(r'<div>(.*)</div>', data)[0]

def youglish(data):
	pass

def yourei(data):
	pass

def neocities(data):
	pass

def find_sentence(source, word):
	scrapers = {
		'massif': {
			'parse': lambda data: massif(data),
			'url': 'https://massif.la/ja/search',
			'params': { 'q': word }
		},
		'youglish': {
			'parse': lambda data: youglish(data),
			'url': 'https://youglish.com/pronounce/{}/japanese'.format(word),
			'params': {}
		},
		'yourei': {
			'parse': lambda data: yourei(data),
			'url': 'https://yourei.jp/{}'.format(word),
			'params': {}
		},
		'neocities': {
			'parse': lambda data: neocities(data),
			'url': 'https://sentencesearch.neocities.org/#{}'.format(word),
			'params': {}
		}
	}
	
	response = requests.get(url = scrapers[source]['url'], params = scrapers[source]['params'])
	sentence = scrapers[source]['parse'](response.text)

	if not sentence or sentence == '':
		raise Exception('')
	return sentence

def remove_punctuation(sentence):
	if sentence[-1] in ['、', '。', '？', '！']:
		return sentence[:-1]
	return sentence

def remove_word_highlight(sentence):
	return re.sub(r'<[^>]*>', '', sentence)

def replace_highlight_style(sentence, highlight_style):
	replaceable =  ['b>', 'em>', 'i>']
	for tag in replaceable:
		sentence = sentence.replace(tag, '{}>'.format(highlight_style))
	return sentence

def update_sentence(note_id, sentence_field, sentence_value):
	invoke('updateNote', note = {
		'id': note_id,
		'fields': {
			sentence_field: sentence_value
		}
	})

def update_tag(note_id, tags):
	invoke('updateNote', note = {
		'id': note_id,
		'tags': tags
	})

def create_query(deck, sentence_field, overwrite):
	query = 'deck:"{}"'.format(deck)
	if not overwrite:
		query += ' "{}":re:^\s*$'.format(sentence_field)
	return query

def main(deck, word_field, sentence_field, overwrite, tag, delay, source, clean_punctuation, clean_word_highlight, highlight_style):
	query = create_query(deck, sentence_field, overwrite)
	note_ids = invoke('findNotes', query = query)

	updated = 0

	for i in range(0, len(note_ids)):
		note_id = note_ids[i]
		word = invoke('notesInfo', notes = [note_id])[0]['fields'][word_field]['value']

		try:
			sentence = find_sentence(source, word)
		except:
			print('[Card {}/{}] Failed to find a sentence for 「{}」!\n'.format(i + 1, len(note_ids), word))
			update_tag(note_id, ['no_sentence'])
			time.sleep(delay)
			continue

		if clean_punctuation:
			sentence = remove_punctuation(sentence)
		
		if clean_word_highlight:
			sentence = remove_word_highlight(sentence)
		else:
			sentence = replace_highlight_style(sentence, highlight_style)
		
		if not debug:
			if tag:
				update_tag(note_id, ['sentence_backfilled'])

			update_sentence(note_id, sentence_field, sentence)

			updated += 1

		print('[Card {}/{}] Updated the sentence for 「{}」 with 「{}」!\n'.format(i + 1, len(note_ids), word, sentence))
		time.sleep(delay)

	print('[Finished] Updated {}/{} cards!'.format(updated, len(note_ids)))

#################################
######### Deck Settings #########
#################################

# The name of the deck to query
deck = 'Mining'

# The field that the word will be read from
word_field = 'Word'

# The field that the sentence will be written to
sentence_field = 'Sentence'

#################################
######### Card Settings #########
#################################

# Enabling this will overwrite cards that already have sentences
overwrite = False

# Enabling this will tag cards with 'sentenced_backfilled'
tag = True

#############################################
######### Sentence Scraper Settings #########
#############################################

# The time to wait between scraping each sentence
delay = 0.5

# The source that sentences will be scraped from
source = 'massif'

# Enabling this will remove final punctuation marks
clean_punctuation = True

# Enabling this will remove any bold/emphasis/italic HTML tags
clean_word_highlight = False

# Setting this will replace the word highlighting style
# 'b' = bold
# 'em' = emphasis
# 'i' = italic
highlight_style = 'b'

############################################
######### Debug Settings (Ignore!) #########
############################################

# Enabling this will stop cards from actually being written to
debug = False

main(deck, word_field, sentence_field, overwrite, tag, delay, source, clean_punctuation, clean_word_highlight, highlight_style)
