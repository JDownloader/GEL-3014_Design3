__author__ = 'Tea'

class Bidict(dict):
    def key_with_value(self, value, default=None):
        for key, val in self.iteritems():
            if val == value:
                return key
        return default

    def keys_with_value(self, value, default=None):
        return [key for key, val in self.iteritems() if val == value]
