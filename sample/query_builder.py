__author__ = 'Tea'
import json
from factbook_mapping_query_types import StringQuery, NestedQuery

class QueryBuilder:

    def __init__(self):
        self.query_items = []

    def withCapital(self, capitalName):
        capital_query = StringQuery('capital',capitalName)
        self.query_items.append(capital_query.category)
        self.query_items.append(capital_query.data)

    def build(self):
        query = NestedQuery(self.query_items)
        return json.dumps(query.complete_query, sort_keys=True)
