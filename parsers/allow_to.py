from parsers.exception import ParserException
from parsers.registry import register_parser
from parsers.host import host_parser
from collections import namedtuple

AllowToRule = namedtuple("AllowToRule", "host port protocol dest")

"""
syntax:
    allow_to <destination host> <port> [protocol]
"""

class AllowToParser(object):

    def parse(self, tokens):
        host = host_parser.current_host 
        if host == None:
            raise ParserException(
                "AllowTo must be inside Host section!")

        if len(tokens) < 3:
            raise ParserException("AllowTo keyword requires an argument!")

        dest = tokens[1]
        port = tokens[2]


        # optional protocol argument
        if 3 in tokens:
            proto = tokens[3]
            if proto != "udp" and proto != "tcp":
                raise ParserException("Unknown protocol %s" % (proto,))
        else:
            proto = "tcp"

        rule = AllowToRule(
            port=port, protocol=proto, dest=dest, host=host)

        return rule

allow_to_parser = AllowToParser()
register_parser("allow_to", allow_to_parser.parse)

