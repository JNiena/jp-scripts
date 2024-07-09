import json
import re
import requests
import urllib.request

def massif(word, exact):
	response = requests.get(url = 'https://massif.la/ja/search', params = {
		'q': '"' + word + '"' if exact else word,
		'fmt': 'json'
	})

	data = json.loads(response.text)

	if data['hits'] > 0:
		return data['results'][0]['highlighted_html']
	return ''

def find_sentence(source, word, exact):
	scrapers = {
		'massif': lambda word, exact: massif(word, exact)
	}

	sentence = scrapers[source](word, exact)

	if not sentence:
		return ''
	return sentence

def remove_punctuation(sentence):
	if sentence[-1] in ['、', '。', '？', '！']:
		return sentence[:-1]
	return sentence

def remove_word_highlight(sentence):
	return re.sub(r'<[^>]*>', '', sentence)

def replace_highlight_style(sentence, highlight_style):
	tags =  ['b>', 'em>', 'i>']
	for tag in tags:
		sentence = sentence.replace(tag, '{}>'.format(highlight_style))
	return sentence

def main(source, destination, match_exact, clean_punctuation, clean_word_highlight, highlight_style):
	with open(source, 'r') as file:
		words = json.loads(file.read())

	output = []

	for i in range(0, len(words)):
		word = words[i]['Word']
		sentence = find_sentence('massif', word, match_exact)

		if clean_punctuation:
			sentence = remove_punctuation(sentence)
		if clean_word_highlight:
			sentence = remove_word_highlight(sentence)
		else:
			sentence = replace_highlight_style(sentence, highlight_style)

		output.append({
			'Word': word,
			'Sentence': sentence
		})

		if sentence != '':
			print('\n{}/{}\nGathered sentence for "{}"\n\tSaved as "{}"'.format(i + 1, len(words), word, sentence))
		else:
			print('\n{}/{}\nFailed to gather sentence for "{}"\n\tSaved as "{}"'.format(i + 1, len(words), word, sentence))

	with open(destination, 'w') as file:
		file.write(json.dumps(output, indent=2))

# The file containing the words to gather example sentences for
source = 'resources/japanese_words.json'

# The file to store the gathered example sentences
destination = 'resources/japanese_example_sentences.json'

# Find sentences that contain the exact word
match_exact = True

# Remove final punctuation marks
clean_punctuation = True

# Remove any bold/emphasis/italic HTML tags
clean_word_highlight = False

# Replace the word highlighting style
# 'b' = bold
# 'em' = emphasis
# 'i' = italic
highlight_style = 'b'

main(source, destination, match_exact, clean_punctuation, clean_word_highlight, highlight_style)
