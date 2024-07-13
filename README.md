# Anki Scripts

## Get Words
A command line tool to export all words from an Anki deck into a text file.

### Usage
`get_words.py [-h] --deck DECK --output OUTPUT --word WORD`

### Args
`--deck`: The name of the deck to query. *

`--output`: The path to output the TXT file. *

`--word`: The field containing the word. *

### Example
`python get_words.py --deck 日本語 --output words.txt --word Word`

## Get Fields
A command line tool that allows for the extraction of Anki fields via JSON format. This script is meant to be used together with [set_fields.py](set_fields.py).

### Usage
`get_fields.py [-h] --deck DECK --output OUTPUT --key KEY [--preview] [--silent] --fields FIELDS [FIELDS ...]`

### Args
`--deck`: The name of the deck to query. *

`--output`: The path to output the JSON file. *

`--key`: The field used to match if the output file already exists. *

‎`--preview`: Preview field mappings.

‎`--silent`: Disable output.

`--fields`: The list of fields to get. *

### Example
`python get_fields.py --deck 日本語 --output fields.json --key Word --fields Word Sentence Frequency`

## Set Fields
A command line tool that allows for the insertion of Anki fields via JSON format. This script is meant to be used together with [get_fields.py](get_fields.py).

### Usage
`set_fields.py [-h] --deck DECK --input INPUT --key KEY [--overwrite] [--preview] [--silent] --fields FIELDS [FIELDS ...]`

### Args
`--deck`: The name of the deck to query. *

`--input`: The path to input the JSON file. *

`--key`: The field used to match. *

`--overwrite`: Overwrite already populated fields.

`--preview`: Preview field mappings.

`--silent`: Disable output.

`--fields`: The list of fields to set. *

### Example
`python set_fields.py --deck 日本語 --input fields.json --key Word --preview --fields Sentence Frequency`

## Sentence Scraper
A command line tool to scrape example sentences from Massif. This script is meant to be used together with [get_fields.py](get_fields.py) and [set_fields.py](set_fields.py).

### Usage
`sentence_scraper.py [-h] --input INPUT --word WORD --sentence SENTENCE [--overwrite] [--silent] [--format {none,bold,italic}] [--exact]`

### Args
`--input`: The path to input the words. *

`--word`: The field containing the word. *

`--sentence`: The field to write the sentence. *

`--overwrite`: Overwrite existing sentences.

`--silent`: Disable output.

`--format`: The word format style to use.

`--exact`: Match the exact word.

### Example
`python sentence_scraper.py --input words.json --word Word --sentence Sentence --exact --format none`

## Vocab Optimizer
A command line tool to tag vocab in Anki based on their relative usefulness.

### Usage
`vocab_optimizer.py [-h] --deck DECK --kanji KANJI --word WORD [--silent]`

### Args
`--deck`: The name of the deck to query. *

`--kanji`: The path to inpout the kanji grid file. *

`--word`: The field containing the word. *

`--silent`: Disable output.

### Example
`python vocab_optimizer.py --deck 日本語 --kanji resources/kanji.json --word Word`

# Adding Example Sentences

Before you start, make sure to back up your deck! The commands below assume the following:
* The deck name is `日本語`.
* The file name to use is `fields.json`.
* The field containing the word is `Word`.
* The field containing the sentence is `Sentence`.

First, use [get_fields.py](get_fields.py) to get all of your words into a JSON file.

`python get_fields.py --deck 日本語 --output fields.json --key Word`

Second, use [sentence_scraper.py](sentence_scraper.py) to add sentences to the same JSON file.

`python sentence_scraper.py --input fields.json --word Word --sentence Sentence`

Third, use [set_fields.py](set_fields.py) to apply the contents of the JSON file to your deck.

`python set_fields.py --deck 日本語 --input fields.json --key Word --fields Sentence`

**It is highly recommended to reuse the same JSON file so you don't have to re-scrape sentences for all of your words every time you rerun the commands!**
