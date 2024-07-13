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

def main(deck, output_path, word_field):
    note_ids = invoke('findNotes', query=f'deck:"{deck}"')

    words = [note['fields'][word_field]['value'] + '\n' for note in invoke('notesInfo', notes=note_ids)]

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(words)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A command line tool to export all words from an Anki deck into a text file.')
    parser.add_argument('--deck', type=str, required=True, help='The name of the deck to query.')
    parser.add_argument('--output', type=str, required=True, help='The path to output the TXT file.')
    parser.add_argument('--word', type=str, required=True, help='The field containing the word.')
    args = parser.parse_args()

    main(args.deck, args.output, args.word)
