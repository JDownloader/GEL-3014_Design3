__author__ = 'Tea'
import json
from factbook_mapping_query_types import StringQuery, NestedQuery, RegexQuery, CompleteQuery

class QueryBuilder:

    def __init__(self):
        self.unwrapped_query_items = []
        self.nested_query_items = []

    def with_independence_date(self, independence_date):
        independence_date_query = StringQuery('independence', ' '.join(independence_date))
        day = self.extract_day(independence_date)
        if day:
            self.unwrapped_query_items.append(RegexQuery(day).regex_query)
        self.append_query(independence_date_query)

    def with_category_data(self, category, data):
        specific_query = StringQuery(category, data)
        self.append_query(specific_query)

    def with_category_only(self, category):
        query = StringQuery(category, '')
        self.unwrapped_query_items.append(query.category)

    def with_regex_query(self, regex):
        self.unwrapped_query_items.append(RegexQuery(regex).regex_query)

    def with_nested_query(self, category, data):
        specific_query = StringQuery(category, data)
        self.nested_query_items.append(NestedQuery([specific_query.category, specific_query.data]).complete_query)

    def build(self):
        nested_query = NestedQuery(self.unwrapped_query_items)
        query = CompleteQuery([nested_query.complete_query] + self.nested_query_items)
        return json.dumps(query.complete_query, sort_keys=True)

    def extract_day(self,independence_date):
        for item in independence_date:
            if len(item) < 3 :
                return item

    def append_query(self, query):
        self.unwrapped_query_items.append(query.category)
        self.unwrapped_query_items.append(query.data)
