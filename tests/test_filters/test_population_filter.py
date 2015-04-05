from collections import OrderedDict
from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import population_filter
from questionanswering.query_builder import QueryBuilder

SENTENCE_CONTAINING_POPULATION_1 = "My population is 32 742."
SENTENCE_CONTAINING_POPULATION_2 = "My population is 32,742. "
SENTENCE_CONTAINING_POPULATION_3 = "My population is 32742. "
SENTENCE_CONTAINING_POPULATION_GREATER_THAN =  "What country has a population greater than 1 300 692 576?"

MAPPED_QUESTION_WITH_POPULATION_SPACED_NUMBER = OrderedDict([('My', 'PRP$'), ('population', 'NN'), ('is', 'VBZ'), ('32', 'CD'), ('742', 'CD'), ('.', '.')])
MAPPED_QUESTION_WITH_GREATER_THAN_INFORMATION = OrderedDict([('What', 'WP'), ('country', 'NN'), ('has', 'VBZ'), ('a', 'DT'), ('population', 'NN'), ('greater', 'NN'), ('than', 'IN'), ('1', 'CD'), ('300', 'CD'), ('692', 'CD'), ('576', 'CD'), ('?', '.')])
POPULATION = '32,742'
POPULATION_RANGE_REGEX = '[1-9],[3-9][0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]'

SENTENCE_NOT_CONTAINING_POPULATION = 'My telephone lines in use are 1.217 million.'

class TestPopulationFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_2, self.query_builder)
        self.dissected_sentence_3 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_2, self.query_builder)
        self.dissected_sentence_4 = question_processor.dissect_sentence(SENTENCE_CONTAINING_POPULATION_GREATER_THAN, self.query_builder)
        self.dissected_sentence_not_containing_population = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_POPULATION, self.query_builder)

    def test_given_dissected_sentence_containing_population_information_when_population_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(population_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(population_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(population_filter.process(self.dissected_sentence_3, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(population_filter.process(self.dissected_sentence_4, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_population_information_when_population_filter_process_then_dont_call_query_builder(self):
        next(population_filter.process(self.dissected_sentence_not_containing_population, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_population_information_when_extracting_population_then_returns_population(self):
        population_2 = question_processor.population_filter.extract_population(next(self.dissected_sentence_2))
        population_3 = question_processor.population_filter.extract_population(next(self.dissected_sentence_3))

        self.assertEqual(population_2, POPULATION)
        self.assertEqual(population_3, POPULATION)

    def test_given_dissected_sentence_containing_population_information_when_extracting_population_from_spaces_number_then_returns_population(self):
        self.assertEqual(population_filter.extract_population_from_spaced_number(MAPPED_QUESTION_WITH_POPULATION_SPACED_NUMBER), POPULATION)

    def test_given_dissected_sentence_containing_population_information_when_extract_greater_than_population_number_then_returns_population_range_regegx(self):
        self.assertEqual(population_filter.extract_greater_than_population_number(MAPPED_QUESTION_WITH_GREATER_THAN_INFORMATION), POPULATION_RANGE_REGEX)