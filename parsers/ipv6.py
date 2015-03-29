from parsers.exception import ParserException
from parsers.registry import register_parser
from collections import namedtuple
from parsers.host import host_parser

IPv6Rule = namedtuple("IPv6Rule", "host addr")

class IPv6Parser(object):

    def parse(self, tokens):
        host = host_parser.current_host 
        if host == None:
            raise ParserException(
                "IPv6 must be inside Host section!")

        if len(tokens) < 2:
            raise ParserException("IPv6 keyword requires an argument!")

        return IPv6Rule(host=host, addr=tokens[1])

_parser = IPv6Parser()
register_parser("ipv6", _parser.parse)
