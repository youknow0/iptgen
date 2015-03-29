from parsers.exception import ParserException
from parsers.registry import register_parser
from collections import namedtuple
from parsers.host import host_parser

IPv4Rule = namedtuple("IPv4Rule", "host addr")

class IPv4Parser(object):

    def parse(self, tokens):
        host = host_parser.current_host 
        if host == None:
            raise ParserException(
                "IPv4 must be inside Host section!")

        if len(tokens) < 2:
            raise ParserException("IPv4 keyword requires an argument!")

        return IPv4Rule(host=host, addr=tokens[1])

_parser = IPv4Parser()
register_parser("ipv4", _parser.parse)
