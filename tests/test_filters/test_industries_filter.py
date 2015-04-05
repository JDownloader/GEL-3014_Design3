from unittest import TestCase
from questionanswering.filters import industries_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_INDUSTRIES_INFORMATION =  "My unemployment rate is greater than 25% and my industries include tourism and footwear."

INDUSTRIES_INFORMATION = ['footwear', 'tourism']

SENTENCE_NOT_CONTAINING_INDUSTRIES_INFORMATION = "What country has religions including 51.3% of protestant and 0.7% of buddhist?"

class TestIndustriesFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_INDUSTRIES_INFORMATION, self.query_builder)
        self.dissected_sentence_not_containing_industries_information= question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_INDUSTRIES_INFORMATION, self.query_builder)

    def test_given_dissected_sentence_containing_industries_information_when_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(industries_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_industries_information_when_filter_process_then_dont_call_query_builder(self):
        next(industries_filter.process(self.dissected_sentence_not_containing_industries_information, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_with_industries_information_when_extracting_then_returns_importation_information(self):
        industries_info = question_processor.industries_filter.extract_industries(next(self.dissected_sentence))
        self.assertEqual(industries_info, INDUSTRIES_INFORMATION)
