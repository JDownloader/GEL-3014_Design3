from unittest import TestCase
from questionanswering.filters import unemployment_rate_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_UNEMPLOYMENT_RATE = "My unemployment rate is 40.6%."

UNEMPLOYMENT_RATE = ['40.6']

SENTENCE_NOT_UNEMPLOYMENT_RATE = "What country has a latitude of 41.00 S?"


class TestUnemploymentRateFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_UNEMPLOYMENT_RATE, self.query_builder)
        self.dissected_sentence_not_containing_unemployment_rate = question_processor.dissect_sentence(SENTENCE_NOT_UNEMPLOYMENT_RATE, self.query_builder)

    def test_given_dissected_sentence_containing_unemployment_rate_when_unemployment_rate_process_then_calls_query_builder(self):
        self.assertTrue(next(unemployment_rate_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_unemployment_rate_when_unemployment_rate_filter_process_then_dont_call_query_builder(self):
        next(unemployment_rate_filter.process(self.dissected_sentence_not_containing_unemployment_rate, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_containing_unemployment_rate_when_extracting_unemployment_rate_then_returns_unemployment_rate(self):
        unemployment_rate = question_processor.unemployment_rate_filter.extract_unemployment_rate(next(self.dissected_sentence))

        self.assertEqual(unemployment_rate, UNEMPLOYMENT_RATE)