from parsers.exception import ParserException
from parsers.registry import register_parser
from parsers.host import host_parser
from collections import namedtuple

AllowOutRule = namedtuple("AllowOutRule", "host port protocol dest")

class AllowOutParser(object):

    allow_out = {}

    def parse(self, tokens):
        host = host_parser.current_host 
        if host == None:
            raise ParserException(
                "AllowOut must be inside Host section!")

        if len(tokens) < 2:
            raise ParserException("AllowOut keyword requires an argument!")

        port = tokens[1]

        # optional protocol argument
        if 3 in tokens:
            proto = tokens[3]
            if proto != "udp" and proto != "tcp":
                raise ParserException("Unknown protocol %s" % (proto,))
        else:
            proto = "tcp"

        # optional destination argument
        dest = None
        if 4 in tokens:
            dest = tokens[4]

        rule = AllowOutRule(
            port=port, protocol=proto, dest=dest, host=host)

        return rule

allow_out_parser = AllowOutParser()
register_parser("allow_out", allow_out_parser.parse)

