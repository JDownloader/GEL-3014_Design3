from unittest import TestCase
from questionanswering.filters import public_debt_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_PUBLIC_DEBT_INFORMATION =  "My public debt is 7.9% of GDP. "

PUBLIC_DEBT_INFORMATION = '7.9'

SENTENCE_NOT_CONTAINING_PUBLIC_DEBT_INFORMATION = "What country has religions including 51.3% of protestant and 0.7% of buddhist?"

class TestPublicDebtFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_PUBLIC_DEBT_INFORMATION, self.query_builder)
        self.dissected_sentence_not_containing_public_debt_information = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_PUBLIC_DEBT_INFORMATION, self.query_builder)

    def test_given_dissected_sentence_containing_public_debt_information_when_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(public_debt_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_public_debt_information_when_filter_process_then_dont_call_query_builder(self):
        next(public_debt_filter.process(self.dissected_sentence_not_containing_public_debt_information, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_with_public_debt_information_when_extracting_then_returns_public_debt_information(self):
        climate_info = public_debt_filter.extract_public_dept(next(self.dissected_sentence))
        self.assertEqual(climate_info, PUBLIC_DEBT_INFORMATION)
