#!/usr/bin/env python3

import argparse
import json
import requests


def find_sentence(word, format_style, exact):
    response = requests.get(
        url = 'https://massif.la/ja/search',
        timeout = 10,
        params = {
            'q': f'"{word}"' if exact else word,
            'fmt': 'json'
        }
    )

    data = json.loads(response.text)

    if data['hits'] < 1:
        return ''

    if format_style == 'bold':
        return data['results'][0]['highlighted_html'].replace('em>', 'b>')
    if format_style == 'italic':
        return data['results'][0]['highlighted_html'].replace('em>', 'i>')

    return data['results'][0]['text']


def main(input_path, overwrite, silent, format_style, exact):
    with open(input_path, 'r', encoding='utf-8') as file:
        array_data = json.loads(file.read())

    for index, object_data in enumerate(array_data):
        word = object_data['Word']

        if 'Sentence' not in object_data or overwrite:
            sentence = find_sentence(word, format_style, exact)

            if sentence != '':
                object_data['Sentence'] = sentence

                with open(input_path, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(array_data, indent=4))

                if not silent:
                    print(f'\n{index + 1}/{len(array_data)}\nGathered sentence for "{word}"\n\tSaved as "{sentence}"')

            elif not silent:
                print(f'\n{index + 1}/{len(array_data)}\nFailed to gather sentence for "{word}"\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A command line tool to scrape example sentences from Massif.')
    parser.add_argument('-i', '--input', type=str, required=True, help='The path to input the words.')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite existing sentences.')
    parser.add_argument('-s', '--silent', action='store_true', help='Disable output.')
    parser.add_argument('-f', '--format', choices=['none', 'bold', 'italic'], required=False, help='The word format style to use.')
    parser.add_argument('-e', '--exact', action='store_true', help='Match the exact expression.')
    args = parser.parse_args()

    main(args.input, args.overwrite, args.silent, args.format, args.exact)
