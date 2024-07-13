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


def main(deck, input_path, key, overwrite, preview, silent, fields):
    note_ids = invoke('findNotes', query=f'deck:"{deck}"')
    notes = invoke('notesInfo', notes=note_ids)

    with open(input_path, 'r', encoding='utf-8') as file:
        array_data = json.loads(file.read())

    matched = 0

    for object_data in array_data:
        for note in notes:
            if note['fields'][key]['value'] != object_data[key]:
                continue

            matched += 1

            if not silent or preview:
                print(f'\n{matched}/{len(notes)}\nMatched "{object_data[key]}" from |{key}| on note [{note['noteId']}]')

            for field in fields:
                if field not in object_data:
                    continue

                if overwrite or note['fields'][field]['value'] == '':
                    if not preview:
                        invoke('updateNote', note={'id': note['noteId'], 'fields': {field: object_data[field]}})

                    if not silent or preview:
                        print(f'\tUpdated |{field}| to "{object_data[field]}"')

            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A command line tool that allows for the insertion of Anki fields via JSON format.')
    parser.add_argument('--deck', type=str, required=True, help='The name of the deck to query.')
    parser.add_argument('--input', type=str, required=True, help='The path to input the JSON file.')
    parser.add_argument('--key', type=str, required=True, help='The field used to match.')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite already populated fields.')
    parser.add_argument('--preview', action='store_true', help='Preview field mappings.')
    parser.add_argument('--silent', action='store_true', help='Disable output.')
    parser.add_argument('--fields', type=str, required=True, nargs='+', help='The list of fields to set.')
    args = parser.parse_args()

    main(args.deck, args.input, args.key, args.overwrite, args.preview, args.silent, args.fields)
