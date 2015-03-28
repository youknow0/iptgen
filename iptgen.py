#!/usr/bin/python

from pprint import PrettyPrinter
from parsers.registry import register_parser, get_parser
from generators.registry import get_generator

import sys
import importlib

import argparse

parser = argparse.ArgumentParser(
    description='iptables/ip6tables generator'
)

parser.add_argument('--generate', 
                    default=sys.stdin,
                    metavar='FILE',
                    type=argparse.FileType('r'),
                    help='Generate iptables rules by reading the given rule file (default: stdin)')

parser.add_argument('--include-origin',
                    dest='include_origin',
                    action='store_true',
                    help='Print the origin line number of each iptables rule in the output')

parser.add_argument('--config',
                    dest='config',
                    required=True,
                    help='the config file to load')

args = parser.parse_args()

execfile(args.config)

rules = []
i = 1
with args.generate as rules_file:
    for l in rules_file:
        tokens = l.split()
        for j, t in enumerate(tokens):
            tokens[j] = t.strip()

        # empty lines
        if len(tokens) < 1:
            i += 1
            continue

        keyword = tokens[0]

        # comments
        if keyword.startswith("#"):
            i += 1
            continue

        if len(tokens) > 0:
            parser = get_parser(keyword)
            rule = parser(tokens)

            generator = get_generator(keyword)

            if args.include_origin:
                rules.append("# origin: line %d" % (i,))

            generated = generator(rule)

            if generated != None:
                rules.append(generated)

        i += 1

for r in rules:
    print r
