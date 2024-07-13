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


def get_fields(deck, fields, log=False):
    note_ids = invoke('findNotes', query=f'deck:{deck}')
    notes = invoke('notesInfo', notes=note_ids)

    array_data = []

    for index, note in enumerate(notes):
        if log:
            print(f'\n{index + 1}/{len(note_ids)}\nGathered fields on note [{note['noteId']}]')

        object_data = {}

        for field in fields:
            object_data[field] = note['fields'][field]['value']

            if log:
                print(f'\tSaved |{field}| as "{object_data[field]}"')

        array_data.append(object_data)

    return array_data


def combine_arrays(first_array, second_array, key):
    final_array = first_array.copy()

    for second_object in second_array:
        match_found = False

        for first_object in final_array:
            if first_object[key] == second_object[key]:
                match_found = True

                for field in second_object:
                    first_object[field] = second_object[field]

                break

        if not match_found:
            final_array.append(second_object)

    return final_array


def read_file_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        try:
            return json.loads(file.read())
        except:
            return False


def main(deck, output_path, key, preview, silent, fields):
    fields = get_fields(deck, fields, not silent or preview)
    old_fields = read_file_json(output_path)

    if old_fields:
        to_write = combine_arrays(old_fields, fields, key)
    else:
        to_write = fields

    if not preview:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(to_write, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A command line tool that allows for the extraction of Anki fields via JSON format.')
    parser.add_argument('-d', '--deck', type=str, required=True, help='The name of the deck to query.')
    parser.add_argument('-o', '--output', type=str, required=True, help='The path to output the JSON file.')
    parser.add_argument('-k', '--key', type=str, required=True, help='The field used to match if the output file already exists.')
    parser.add_argument('-p', '--preview', action='store_true', help='Preview field mappings.')
    parser.add_argument('-s', '--silent', action='store_true', help='Disable output.')
    parser.add_argument('-f', '--fields', type=str, required=True, nargs='+', help='The list of fields to get.')
    args = parser.parse_args()

    main(args.deck, args.output, args.key, args.preview, args.silent, args.fields)
