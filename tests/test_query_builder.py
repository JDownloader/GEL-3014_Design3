from questionanswering import query_builder
from unittest import TestCase

DUMMY_CATEGORY = "dummy category"
DUMMY_DATA  = "dummy data"
DUMMY_REGEX = '!"/$%?&*()'
EXPECTED_CATEGORY_DATA_QUERY  = [{'query_string': {'query': 'dummy category', 'default_field': 'category'}},{'query_string': {'default_field': 'data', 'query': 'dummy data'}}]
EXPECTED_CATEGORY_QUERY = [{'query_string': {'query': 'dummy category', 'default_field': 'category'}}]
EXPECTED_REGEX_QUERY = [{'regexp': {'data': '!"/$%?&*()'}}]

class TestQueryBuilder(TestCase):

    def setUp(self):
        self.query_builder = query_builder.QueryBuilder()

    def test_given_category_and_data_when_calling_with_category_data_then_appends_new_query_to_query_items(self):
        self.query_builder.with_category_data(DUMMY_CATEGORY, DUMMY_DATA)
        self.assertListEqual(EXPECTED_CATEGORY_DATA_QUERY, self.query_builder.query_items)

    def test_given_category_when_calling_with_category_data_then_appends_new_category_to_query_items(self):
        self.query_builder.with_category_only(DUMMY_CATEGORY)
        self.assertListEqual(EXPECTED_CATEGORY_QUERY, self.query_builder.query_items)

    def test_given_regex_when_calling_with_regex_query_then_appends_new_regex_to_query_items(self):
        self.query_builder.with_regex_query(DUMMY_REGEX)
        self.assertListEqual(EXPECTED_REGEX_QUERY, self.query_builder.query_items)

