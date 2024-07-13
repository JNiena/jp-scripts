# Anki Scripts

## Get Fields
A command line tool that allows for the extraction of Anki fields via JSON format. This script is meant to be used together with [set_fields.py](set_fields.py).

### Usage
`python get_fields.py [-h] -d DECK -o OUTPUT -k KEY [-p] [-s] -f FIELDS [FIELDS ...]`

### Args
`-d | --deck`: The name of the deck to query. *

`-o | --output`: The path to output the JSON file. *

`-k | --key`: The field used to match if the output file already exists. *

‎`-p | --preview`: Preview field mappings.

‎`-s | --silent`: Disable output.

`-f | --fields`: The list of fields to get. *

### Example
`python get_fields.py --deck 日本語 --output fields.json --key Word --fields Word Sentence Frequency`

## Set Fields
A command line tool that allows for the insertion of Anki fields via JSON format. This script is meant to be used together with [get_fields.py](get_fields.py).

### Usage
`python set_fields.py [-h] -d DECK -i INPUT -k KEY [-o] [-p] [-s] -f FIELDS [FIELDS ...]`

### Args
`-d | --deck`: The name of the deck to query. *

`-i | --input`: The path to input the JSON file. *

`-k | --key`: The field used to match. *

`-o | --overwrite`: Overwrite already populated fields.

`-p | --preview`: Preview field mappings.

`-s | --silent`: Disable output.

`-f | --fields`: The list of fields to set. *

### Example
`python set_fields.py --deck 日本語 --input fields.json --key Word --preview --fields Sentence Frequency`

## Sentence Scraper
A command line tool to scrape example sentences from Massif. This script is meant to be used together with [get_fields.py](get_fields.py) and [set_fields.py](set_fields.py).

### Usage
`python sentence_scraper.py [-h] -i INPUT [-o] [-s] [-f {none,bold,italic}] [-e]`

### Args
`-i | --input`: The path to input the words. *

`-o | --overwrite`: Overwrite existing sentences.

`-s | --silent`: Disable output.

`-f | --format`: The word format style to use.

`-e | --exact`: Match the exact expression.

### Example
`python sentence_scraper.py --input words.json --exact --format none`
