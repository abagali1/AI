#!/usr/bin/env python3
import json
import functools
import argparse
import requests
import multiprocessing

URL = "https://www.dictionary.com/browse/{0}?s=t"
DEFAULT_MAX_PROCESSES = multiprocessing.cpu_count()
dictionary = {}


def extract_word(resp, word):
    index = resp.find('<meta name="description" content="')
    data = resp[index:]
    data = data[:data.index("\n")]
    data = data[data.index("content=") + 22 + len(word):-12]
    return data


def get_words(args):
    words = open(args.filename, 'r').read().splitlines()
    for i, word in enumerate(words):
        r = requests.get(URL.format(word))
        definition = extract_word(r.text, word)
        print(i)



def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=get_words)
    parser.add_argument("filename", help="path to dictionary file")
    parser.add_argument("max_definitions", help="max amount of definitions to capture for each word", default=1)
    parser.add_argument("processes", help="max amount of proccess to spawn", default=DEFAULT_MAX_PROCESSES)
    

    args = parser.parse_args()
    if args.processes > DEFAULT_MAX_PROCESSES:
        print("Cannot spawn more processes than available cores")
        return 1
    if args.max_definitions < 1:
        print("Cannot have less than 1 definition for each word")
        return 1
    args.func(args)


if __name__ == '__main__':
    main()
