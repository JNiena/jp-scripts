#!/usr/bin/env python3

import argparse
import json
import urllib.request


def request(action, **params):
    return { 'action': action, 'params': params, 'version': 6 }


def invoke(action, **params):
    request_json = json.dumps(request(action, **params)).encode('utf-8')

    with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', request_json)) as url:
        response = json.load(url)

    if len(response) != 2:
        raise Exception('The response has an unexpected number of fields.')
    if 'error' not in response:
        raise Exception('The response is missing a required error field.')
    if 'result' not in response:
        raise Exception('The response is missing a required result field.')
    if response['error'] is not None:
        raise Exception(response['error'])

    return response['result']


def tag_note(note_id, tags):
    invoke('updateNote', note={'id': note_id, 'tags': tags})


def find_unknown_kanji(kanji_grid_path):
    unknown_kanji = []

    with open(kanji_grid_path, encoding='utf-8') as file:
        kanji_grid = json.load(file)['units']

    for kanji in kanji_grid:
        if kanji_grid[kanji][2] + kanji_grid[kanji][3] == 0:
            unknown_kanji.append(kanji)

    return unknown_kanji


def is_useless_word(word, unknown_kanji):
    for kanji in unknown_kanji:
        if kanji in word:
            return False

    return True


def main(deck, word_field, kanji_grid_path, silent):
    unknown_kanji = find_unknown_kanji(kanji_grid_path)

    note_ids = invoke('findNotes', query = f'deck:"{deck}" is:new')
    notes = invoke('notesInfo', notes = note_ids)

    for index, note in enumerate(notes):
        word = note['fields'][word_field]['value']

        useless = is_useless_word(word, unknown_kanji)

        if useless:
            tag_note(note['noteId'], ['useless'])
        else:
            tag_note(note['noteId'], ['useful'])

        if not silent:
            print(f'\n{index + 1}/{len(notes)}\nClassified word "{word}" as {"useless" if useless else "useful"}.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A command line tool to tag vocab in Anki based on their relative usefulness.')
    parser.add_argument('--deck', type=str, required=True, help='The name of the deck to query.')
    parser.add_argument('--kanji', type=str, required=True, help='The path to input the kanji grid file.')
    parser.add_argument('--word', type=str, required=True, help='The field containing the word.')
    parser.add_argument('--silent', action='store_true', help='Disable output.')
    args = parser.parse_args()

    main(args.deck, args.word, args.kanji, args.silent)
