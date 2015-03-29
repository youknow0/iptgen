#!/usr/bin/python
from __future__ import print_function
from __future__ import unicode_literals 

from pprint import PrettyPrinter
from parsers.registry import register_parser, get_parser
from parsers.exception import ParserException
from generators.exception import GeneratorException
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

# load the config file
with open(args.config) as c:
    code = compile(c.read(), args.config, 'exec')
    exec(code)

def error_out(msg):
    print ("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)

def error_line(msg, line):
    error_out("in rule file, line %d: %s" % (line, msg))

rules = []
i = 1
with args.generate as rules_file:
    for l in rules_file:
        tokens = l.split()

        tokens = [t.strip() for t in tokens]

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

            try:
                parser = get_parser(keyword)

                rule = parser(tokens)

                generator = get_generator(keyword)

                generated = generator(rule)
    
                # only add rule to output if the generator actually
                # produced output
                if generated != None:
                    # include origin
                    if args.include_origin:
                        rules.append("# origin: line %d" % (i,))
                    rules.append(generated)

            except ParserException as e:
                error_line(e, i)
            except GeneratorException as e:
                error_line(e, i)

        i += 1

for r in rules:
    print(r)

