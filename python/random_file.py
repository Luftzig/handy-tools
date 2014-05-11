#!/usr/bin/python
import argparse
import re
import random
import numpy.random as nprandom


def define_arguments():
    parser = argparse.ArgumentParser(description="Create a file with random content of a given size")
    parser.add_argument('size', help='the request file size, e.g. 2M (2000,000 bytes), 1Ki (1024 bytes)')
    parser.add_argument('filename', nargs='*')
    parser.add_argument('-S', '--seed', dest='seed', help='optional seed value')
    return parser


def parse_arguments():
    parser = define_arguments()
    return parser.parse_args()


def process_weight(weight_string):
    return {
        "b": 1,
        "bi": 1,
        "k": 1000,
        "ki": 1024,
        "m": 1000 ** 2,
        "mi": 1024 ** 2,
        'g': 1000 ** 3,
        'gi': 1024 ** 3
    }.get(weight_string.lower())


def convert_to_bytes(size):
    match = re.match('(?P<number>\d+)(?P<weight>[bBkKmMgG]i?)?', size)
    if match is None:
        raise argparse.ArgumentError('size', 'argument size cannot be parsed')
    weight = process_weight(match.group('weight'))
    number = int(match.group('number'))
    return weight * number


def create_file(filename, size_in_bytes):
    with open(filename, 'wb') as file_output:
        file_output.write(nprandom.bytes(size_in_bytes))


def create_files(arguments):
    size_in_bytes = convert_to_bytes(arguments.size)
    files = arguments.filename
    if not files or len(files) < 1:
        files = ['random_{}.data'.format(arguments.size)]
    if arguments.seed:
        nprandom.seed(hash(arguments.seed))

    for filename in files:
        create_file(filename, size_in_bytes)


if __name__ == '__main__':
    arguments = parse_arguments()
    create_files(arguments)
    exit(0)
