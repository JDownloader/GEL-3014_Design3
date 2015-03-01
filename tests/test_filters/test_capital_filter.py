from unittest import TestCase
from questionanswering.filters import capital_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_CAPITAL_1 = 'My capital name starts with Ath and ends with ens.'
SENTENCE_CONTAINING_CAPITAL_2 = "My capital name starts with Moga."
SENTENCE_CONTAINING_CAPITAL_3 = "My death rate is greater than 13 death/1000 and my capital starts with Mos."
SENTENCE_CONTAINING_CAPITAL_4 = "What country has Yaounde as its capital?"

CAPITAL_1 = "Athens"
CAPITAL_2 = "Moga*"
CAPITAL_3 = "Mos*"
CAPITAL_4 = "Yaounde"

SENTENCE_NOT_CONTAINING_CAPITAL = "What country has a latitude of 41.00 S?"

class TestCapitalFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_CAPITAL_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_CAPITAL_2, self.query_builder)
        self.dissected_sentence_3 = question_processor.dissect_sentence(SENTENCE_CONTAINING_CAPITAL_3, self.query_builder)
        self.dissected_sentence_4 = question_processor.dissect_sentence(SENTENCE_CONTAINING_CAPITAL_4, self.query_builder)
        self.dissected_sentence_not_containing_capital = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_CAPITAL, self.query_builder)

    def test_given_dissected_sentence_containing_capital_information_when_capital_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(capital_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(capital_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(capital_filter.process(self.dissected_sentence_3, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(capital_filter.process(self.dissected_sentence_4, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_capital_information_when_capital_filter_process_then_dont_call_query_builder(self):
        next(capital_filter.process(self.dissected_sentence_not_containing_capital, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_containing_capital_information_when_extracting_capital_name_then_returns_capital_name(self):
        capital_1 =  question_processor.capital_filter.extract_capital_name(next(self.dissected_sentence_1))
        capital_2 =  question_processor.capital_filter.extract_capital_name(next(self.dissected_sentence_2))
        capital_3 =  question_processor.capital_filter.extract_capital_name(next(self.dissected_sentence_3))
        capital_4 =  question_processor.capital_filter.extract_capital_name(next(self.dissected_sentence_4))

        self.assertEqual(capital_1, CAPITAL_1)
        self.assertEqual(capital_2, CAPITAL_2)
        self.assertEqual(capital_3, CAPITAL_3)
        self.assertEqual(capital_4, CAPITAL_4)
