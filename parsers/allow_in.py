from parsers.exception import ParserException
from parsers.registry import register_parser
from parsers.host import host_parser
from collections import namedtuple

AllowInRule = namedtuple("AllowInRule", "host port protocol")

class AllowInParser(object):

    def parse(self, tokens):
        host = host_parser.current_host 
        if host == None:
            raise ParserException(
                "AllowIn must be inside Host section!")

        if len(tokens) < 2:
            raise ParserException("AllowIn keyword requires an argument!")

        port = tokens[1]

        # optional protocol argument
        if len(tokens) >= 3:
            proto = tokens[2]
            if proto != "udp" and proto != "tcp":
                raise ParserException("Unknown protocol %s" % (proto,))
        else:
            proto = "tcp"

        rule = AllowInRule(port=port, protocol=proto, host=host)

        return rule

allow_in_parser = AllowInParser()
register_parser("allow_in", allow_in_parser.parse)

