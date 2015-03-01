from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import population_filter
from questionanswering.query_builder import QueryBuilder

SENTENCE_CONTAINING_POPULATION_1 = "My population is 32 742."
SENTENCE_CONTAINING_POPULATION_2 = "My population is 32,742. "
SENTENCE_CONTAINING_POPULATION_3 = "My population is 32742. "

POPULATION = '32,742'

SENTENCE_NOT_CONTAINING_POPULATION = 'My telephone lines in use are 1.217 million.'

class TestPopulationFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.extract_from_spaced_number_mock = question_processor.population_filter.extract_population_from_spaced_number = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_2, self.query_builder)
        self.dissected_sentence_3 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_2, self.query_builder)
        self.dissected_sentence_not_containing_population = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_POPULATION, self.query_builder)

    def test_given_dissected_sentence_containing_population_information_when_population_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(population_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(population_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(population_filter.process(self.dissected_sentence_3, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_population_information_when_population_filter_process_then_dont_call_query_builder(self):
        next(population_filter.process(self.dissected_sentence_not_containing_population, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_population_information_when_extracting_population_then_returns_population(self):
        self.assertTrue(question_processor.population_filter.extract_population(next(self.dissected_sentence_1)), self.extract_from_spaced_number_mock.extract_population_from_spaced_number.called)
        population_2 = question_processor.population_filter.extract_population(next(self.dissected_sentence_2))
        population_3 = question_processor.population_filter.extract_population(next(self.dissected_sentence_3))

        self.assertEqual(population_2, POPULATION)
        self.assertEqual(population_3, POPULATION)
