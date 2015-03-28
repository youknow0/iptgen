from parsers.exception import ParserException
from parsers.registry import register_parser
from collections import namedtuple

HostRule = namedtuple("HostRule", "host")

class HostParser(object):

    hosts = []
    current_host = None

    def parseHost(self, tokens):
        if self.current_host != None:
            raise ParserException(
                'Host section "%s" was not closed!' % 
                    (self.current_host,))

        if len(tokens) < 2:
            raise ParserException("Host keyword requires an argument!")

        host = tokens[1]

        if host in self.hosts:
            raise ParserException(
                'Duplicate host section for "%s"' % (host,))

        self.hosts.append(host)

        self.current_host = host

        return HostRule(host=host)

    def parseEndHost(self, tokens):
        if self.current_host == None:
            raise ParserException(
                "Unexpected end host!")

        self.current_host = None

        return ()

host_parser = HostParser()
register_parser("host", host_parser.parseHost)
register_parser("end_host", host_parser.parseEndHost)
