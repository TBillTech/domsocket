#!/usr/bin/python

import argparse
import os
from os.path import abspath

def update_word(word):
    first_letter = word[0]
    if word[0].isupper():
        return word
    updated_word = []
    for char in word:
        if char.isupper():
            updated_word.append('_')
            updated_word.append(char.lower())
        else:
            updated_word.append(char)
    return updated_word

def get_words(input_string):
    word = []
    for char in input_string:
        if char.isalpha():
            word.append(char)
        else:
            if word:
                yield update_word(word)
            word = [char]
            yield word
            word = []
    if word:
        yield update_word(word)


def convert_string(input_string):
    output_chars = []

    for word in get_words(input_string):
        output_chars += word

    return ''.join(output_chars)

def convert(file_name):
    with open(file_name, 'r') as to_convert:
        input_string = to_convert.read()

    converted_string = convert_string(input_string)

    with open(file_name, 'w+') as to_write:
        to_write.write(converted_string)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert from camelCase to under_score')
    
    parser.add_argument('file_names', metavar='Files', type=str,
                        nargs='+', help='files to convert')

    args = parser.parse_args()
    
    for file_name in args.file_names:
        print('converting %s' % (file_name,))
        convert(abspath(file_name))
