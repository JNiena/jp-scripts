#!/usr/bin/env python3

import argparse
from konoha import WordTokenizer


def generate_kanji():
    kanji = []

    for start, end in [(0x4E00, 0x9FFF), (0x3400, 0x4DBF), (0xF900, 0xFAFF), (0x20000, 0x2A6DF), (0x2A700, 0x2B73F), (0x2B740, 0x2B81F), (0x2B820, 0x2CEAF), (0x2CEB0, 0x2EBEF)]:
        kanji.extend(chr(code) for code in range(start, end + 1))

    return set(kanji)


def generate_kana():
    hiragana = [chr(code) for code in range((0x3040, 0x309F)[0], (0x3040, 0x309F)[1] + 1)]
    katakana = [chr(code) for code in range((0x30A0, 0x30FF)[0], (0x30A0, 0x30FF)[1] + 1)]

    return set(hiragana + katakana)


def main(input_path, output_path, kanji_grid_path):
    kanji = generate_kanji()
    kana = generate_kana()

    with open(kanji_grid_path, 'r', encoding='utf-8') as file:
        known_kanji = set(file.read().splitlines())

    with open(input_path, 'r', encoding='utf-8') as file:
        book = file.read()

    tokenizer = WordTokenizer('MeCab')

    unique_words = {str(word) for word in tokenizer.tokenize(book) if all(char in kanji or char in kana for char in str(word))}
    interest_words = set()

    for word in unique_words:
        for char in word:
            if char not in known_kanji | kana:
                interest_words.add(word + '\n')
                break

    with open(output_path, "w", encoding='utf-8') as file:
        file.writelines(interest_words)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A command line tool that finds interest words.')
    parser.add_argument('--input', type=str, required=True, help='The path to input the book text file.')
    parser.add_argument('--output', type=str, required=True, help='The path to output the interest words.')
    parser.add_argument('--kanji', type=str, required=True, help='The path to input the kanji grid file.')
    args = parser.parse_args()

    main(args.input, args.output, args.kanji)
