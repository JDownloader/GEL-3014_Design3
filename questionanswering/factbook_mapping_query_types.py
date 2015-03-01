class StringQuery:

    def __init__(self, category, data):
        self.category = {"query_string": {"default_field": "category", "query": category}}
        self.data = {"query_string": {"default_field": "data", "query": data}}

class NestedQuery:

    def __init__(self, items):
        self.complete_query = {"query":{"bool":{"must":[{"nested":{"path":"fields","query":{"bool":{"must":[items]}}}}]}}}

class RegexQuery:

    def __init__(self, regex):
        self.regex_query = {"regexp":{"data": regex}}