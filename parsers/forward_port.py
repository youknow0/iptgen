from parsers.exception import ParserException
from parsers.registry import register_parser
from collections import namedtuple
from parsers.host import host_parser

ForwardPortRule = namedtuple("ForwardPortRule", "host port protocol ip_from ip_to")

"""
syntax:
    forward_port <ip to forward from> <ip to forward to> <port  to forward> [proto]
"""

class ForwardPortParser(object):

    def parse(self, tokens):
        host = host_parser.current_host 
        if host == None:
            raise ParserException(
                "ForwardPort must be inside Host section!")

        if len(tokens) < 4:
            raise ParserException(
                "ForwardPort keyword requires three arguments!")

        ip_from = tokens[1]
        ip_to = tokens[2]
        port = tokens[3]

        # optional protocol argument
        if len(tokens) >= 5:
            proto = tokens[4]
            if proto != "udp" and proto != "tcp":
                raise ParserException("Unknown protocol %s" % (proto,))
        else:
            proto = "tcp"

        rule = ForwardPortRule(
            port=port, protocol=proto, host=host, ip_from=ip_from, 
                ip_to=ip_to)

        return rule

forward_port_parser = ForwardPortParser()
register_parser("forward_port", forward_port_parser.parse)

