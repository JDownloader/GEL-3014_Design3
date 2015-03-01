from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import national_symbol_filter
from questionanswering.query_builder import QueryBuilder

SENTENCE_CONTAINING_NATIONAL_SYMBOL_1 = "One national symbol of this country is the edelweiss."
SENTENCE_CONTAINING_NATIONAL_SYMBOL_2 = "The lotus blossom is the national symbol of this country."
SENTENCE_CONTAINING_NATIONAL_SYMBOL_3 = "My national symbol is the elephant."

NATIONAL_SYMBOL_1 = ['edelweiss']
NATIONAL_SYMBOL_2 = ['lotus', 'blossom']
NATIONAL_SYMBOL_3 = ['elephant']

SENTENCE_NOT_CONTAINING_NATIONAL_SYMBOL = 'My telephone lines in use are 1.217 million.'


class TestNationalSymbolFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_NATIONAL_SYMBOL_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_NATIONAL_SYMBOL_2, self.query_builder)
        self.dissected_sentence_3 = question_processor.dissect_sentence(SENTENCE_CONTAINING_NATIONAL_SYMBOL_3, self.query_builder)
        self.dissected_sentence_not_national_symbol = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_NATIONAL_SYMBOL, self.query_builder)

    def test_given_dissected_sentence_containing_national_symbol_information_when_national_symbol_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(national_symbol_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(national_symbol_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(national_symbol_filter.process(self.dissected_sentence_3, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_national_symbol_information_when_national_symbol_filter_process_then_dont_call_query_builder(self):
        next(national_symbol_filter.process(self.dissected_sentence_not_national_symbol, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_national_symbol_information_when_extracting_national_symbol_then_returns_national_symbol(self):
        national_symbol_1 = question_processor.national_symbol_filter.extract_national_symbol(next(self.dissected_sentence_1))
        national_symbol_2 = question_processor.national_symbol_filter.extract_national_symbol(next(self.dissected_sentence_2))
        national_symbol_3 = question_processor.national_symbol_filter.extract_national_symbol(next(self.dissected_sentence_3))

        self.assertEqual(national_symbol_1, NATIONAL_SYMBOL_1)
        self.assertEqual(national_symbol_2, NATIONAL_SYMBOL_2)
        self.assertEqual(national_symbol_3, NATIONAL_SYMBOL_3)