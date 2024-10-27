#!/usr/bin/sh

# Change this to the name of your deck.
deck_name="日本語"

# Change this to the field that contains the word in your deck.
word_field="Word"

# Change this to the field that contains the sentence in your deck.
sentence_field="Sentence"

cache_path="cache.json"

[[ -e $cache_path ]] && cp $cache_path "$cache_path".backup

./get_fields.py --deck $deck_name --output $cache_path --key $word_field --fields $word_field $sentence_field
./sentence_scraper.py --input $cache_path --word $word_field --sentence $sentence_field --exact
./set_fields.py --deck $deck_name --input $cache_path --key $word_field --fields $sentence_field
