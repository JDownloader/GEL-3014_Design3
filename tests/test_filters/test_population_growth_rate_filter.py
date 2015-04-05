from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import population_growth_rate_filter
from questionanswering.query_builder import QueryBuilder


SENTENCE_CONTAINING_POPULATION_GROWTH_RATE_1 = "My population growth rate is between 1.44% and 1.47%."
SENTENCE_CONTAINING_POPULATION_GROWTH_RATE_2 = "What country has a population growth rate of 1.46%?"

POPULATION_GROWTH_RATE_2 = ['1.46']

SENTENCE_NOT_CONTAINING_POPULATION_GROWTH_RATE = 'My telephone lines in use are 1.217 million.'


class TestPopulationGrowthRateFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.process_between_mock = question_processor.population_growth_rate_filter.process_between_growth_rate = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_GROWTH_RATE_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_GROWTH_RATE_2, self.query_builder)
        self.dissected_sentence_not_containing_population_growth_rate = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_POPULATION_GROWTH_RATE, self.query_builder)

    def test_given_dissected_sentence_containing_population_growth_rate_information_when_country_population_growth_rate_process_then_calls_query_builder(self):
        self.assertTrue(next(population_growth_rate_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(population_growth_rate_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_population_growth_rate_information_when_population_growth_rate_filter_process_then_dont_call_query_builder(self):
        next(population_growth_rate_filter.process(self.dissected_sentence_not_containing_population_growth_rate, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_population_growth_rate_when_extracting_population_growth_rate_name_then_returns_population_growth_rate(self):
        self.assertTrue(question_processor.population_growth_rate_filter.process(self.dissected_sentence_1, self.query_builder), self.process_between_mock.process_between_growth_rate.called)
        population_growth_rate = question_processor.population_growth_rate_filter.extract_growth_rate(next(self.dissected_sentence_2))

        self.assertEqual(population_growth_rate, POPULATION_GROWTH_RATE_2)