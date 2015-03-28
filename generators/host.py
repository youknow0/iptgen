from generators.registry import register_generator

class HostGenerator(object):

    def generate(self, rule):
        return "### rules for %s" % (rule.host,)


_gen = HostGenerator()
register_generator("host", _gen.generate)
register_generator("end_host", lambda x: "")
