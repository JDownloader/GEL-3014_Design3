from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import electricity_production_filter
from questionanswering.query_builder import QueryBuilder


SENTENCE_CONTAINING_ELECTRICITY_PRODUCTION_INFORMATION = "My electricity production is between 600 and 650 billion kWh."

NUMBERS = ['billion', '600', '650']
NUMBERS_WITHOUT_UNITY = ['600', '650']
MIN_AND_MAX = ('600', '650')
REGEX_RESULTS = ('billion', '6[0-5][0-9].+&.*')

SENTENCE_NOT_CONTAINING_ELECTRICITY_PRODUCTION_INFORMATION = 'My telephone lines in use are 1.217 million.'


class TestElectricityProductionFilter(TestCase):

    def setUp(self):
        self.query_builder_with_category_data = QueryBuilder().with_category_data = mock.MagicMock()
        self.query_builder_with_regex_query = QueryBuilder().with_category_data = mock.MagicMock()

        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_ELECTRICITY_PRODUCTION_INFORMATION, self.query_builder_with_category_data)
        self.dissected_sentence_with_regex_call = question_processor.dissect_sentence(SENTENCE_CONTAINING_ELECTRICITY_PRODUCTION_INFORMATION, self.query_builder_with_regex_query)
        self.dissected_sentence_not_containing_electricity_information = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_ELECTRICITY_PRODUCTION_INFORMATION, self.query_builder_with_category_data)

    def test_given_dissected_sentence_containing_electricity_information_information_when_process_then_calls_query_builder(self):
        self.assertTrue(next(electricity_production_filter.process(self.dissected_sentence, self.query_builder_with_category_data)), self.query_builder_with_category_data.with_category_data.called)
        self.assertTrue(next(electricity_production_filter.process(self.dissected_sentence_with_regex_call, self.query_builder_with_regex_query)), self.query_builder_with_regex_query.with_regex_query.called)


    def test_given_dissected_sentence_not_containing_electricity_information_when_process_then_dont_call_query_builder(self):
        next(electricity_production_filter.process(self.dissected_sentence_not_containing_electricity_information, self.query_builder_with_category_data))
        self.assertFalse(self.query_builder_with_category_data.with_category_data.called)

    def test_given_dissected_sentence_containing_electricity_when_extracting_then_returns_electricity_information(self):
        self.assertEqual(electricity_production_filter.extract_electricity_production_information(next(self.dissected_sentence)), REGEX_RESULTS)

    def test_given_a_list_of_numbers_when_extracting_unity_then_returns_only_unity(self):
        self.assertEqual(electricity_production_filter.extract_unity(NUMBERS), REGEX_RESULTS[0])

    def test_given_range_numbers_when_creating_regex_then_returns_regex_for_number_range(self):
        self.assertEqual(electricity_production_filter.create_regex_with_numbers(MIN_AND_MAX), REGEX_RESULTS[1])

    def test_given_range_numbers_when_process_min_and_max_from_two_numbers_then_returns_min_max_tuple(self):
        self.assertEqual(electricity_production_filter.process_min_and_max_from_two_numbers(NUMBERS_WITHOUT_UNITY), MIN_AND_MAX)

