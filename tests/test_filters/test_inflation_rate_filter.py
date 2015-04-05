from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import inflation_rate_filter
from questionanswering.query_builder import QueryBuilder


SENTENCE_CONTAINING_INFLATION_RATE = "What country has an inflation rate between 0.3% and 0.5%?"

SENTENCE_NOT_CONTAINING_POPULATION_GROWTH_RATE = 'My telephone lines in use are 1.217 million.'


class TestInflationFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.process_between_mock = question_processor.inflation_rate_filter.extract_inflation_rate = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_INFLATION_RATE, self.query_builder)
        self.dissected_sentence_not_containing_inflation_rate = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_POPULATION_GROWTH_RATE, self.query_builder)

    def test_given_dissected_sentence_containing_inflation_rate_information_when_process_then_calls_query_builder(self):
        self.assertTrue(next(inflation_rate_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_inflation_rate_information_when_process_then_dont_call_query_builder(self):
        next(inflation_rate_filter.process(self.dissected_sentence_not_containing_inflation_rate, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_inflation_rate_when_extracting_rate_then_calls_process_between_rate(self):
        self.assertTrue(question_processor.inflation_rate_filter.process(self.dissected_sentence, self.query_builder), self.process_between_mock.extract_inflation_rate.called)

