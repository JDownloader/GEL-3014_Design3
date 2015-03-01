__author__ = 'Tea'
import json
from factbook_mapping_query_types import StringQuery, NestedQuery, RegexQuery

class QueryBuilder:

    def __init__(self):
        self.query_items = []

    def with_independence_date(self, independence_date):
        independence_date_query = StringQuery('independence', ' '.join(independence_date))
        day = self.extract_day(independence_date)
        if day:
            self.query_items.append(RegexQuery(day).regex_query)
        self.append_query(independence_date_query)

    def with_category_data(self, category, data):
        specific_query = StringQuery(category, data)
        self.append_query(specific_query)

    def build(self):
        query = NestedQuery(self.query_items)
        # print query.complete_query
        return json.dumps(query.complete_query, sort_keys=True)

    def extract_day(self,independence_date):
        for item in independence_date:
            if len(item) < 3 :
                return item

    def append_query(self, query):
        self.query_items.append(query.category)
        self.query_items.append(query.data)
