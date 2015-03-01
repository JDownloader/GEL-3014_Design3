__author__ = 'Tea'

class Bidict(dict):
    def key_with_value(self, value, default=None):
        for key, val in self.iteritems():
            if val == value:
                return key
        return default

    def keys_with_value(self, value, default=None):
        return [key for key, val in self.iteritems() if val == value]

    def keys_with_values(self, values):
        keys = []
        for value in values:
            keys += self.keys_with_value(value)
        return keys
