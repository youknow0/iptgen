from generators.registry import register_generator

class AddressGenerator(object):

    addrs = {}

    def generate(self, rule):

        host = rule.host
        addr = rule.addr 

        if not host in self.addrs:
            self.addrs[host] = []

        self.addrs[host].append(addr)

        return None

addr_generator = AddressGenerator()
