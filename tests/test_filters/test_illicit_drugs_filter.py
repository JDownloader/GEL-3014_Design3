from unittest import TestCase
from questionanswering.filters import illicit_drugs_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_ILLICIT_DRUGS_INFORMATION =  "What country has illicit drugs activities including a transshipment point for cocaine from South America to North America and illicit cultivation of cannabis?"

ILLICIT_DRUGS_INFORMATION = ['a', 'transshipment', 'point', 'for', 'cocaine', 'from', 'South', 'America', 'to', 'North', 'and', 'cultivation', 'of', 'cannabis', '?']

SENTENCE_NOT_CONTAINING_ILLICIT_DRUGS_INFORMATION = "What country has a latitude of 41.00 S?"

class TestIllicitDrugsFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_ILLICIT_DRUGS_INFORMATION, self.query_builder)
        self.dissected_sentence_not_containing_illicit_drugs_information = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_ILLICIT_DRUGS_INFORMATION, self.query_builder)

    def test_given_dissected_sentence_containing_illicit_drugs_information_when_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(illicit_drugs_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_illicit_drugs_information_when_filter_process_then_dont_call_query_builder(self):
        next(illicit_drugs_filter.process(self.dissected_sentence_not_containing_illicit_drugs_information, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_with_illicit_drugs_information_when_extracting_then_returns_illicit_drugs_information(self):
        illicit_drugs_info = question_processor.illicit_drugs_filter.extract_illicit_drugs_statement(next(self.dissected_sentence))
        self.assertEqual(illicit_drugs_info, ILLICIT_DRUGS_INFORMATION)
