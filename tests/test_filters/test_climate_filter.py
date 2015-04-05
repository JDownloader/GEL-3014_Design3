from unittest import TestCase
from questionanswering.filters import climate_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_CLIMATE_INFORMATION =  "What country has a tropical climate and has a capital that starts with the letters Phn?"

CLIMATE_INFORMATION = ['tropical']

SENTENCE_NOT_CONTAINING_CLIMATE_INFORMATION = "What country has religions including 51.3% of protestant and 0.7% of buddhist?"

class TestClimateFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_CLIMATE_INFORMATION, self.query_builder)
        self.dissected_sentence_not_containing_importation_information = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_CLIMATE_INFORMATION, self.query_builder)

    def test_given_dissected_sentence_containing_climate_information_when_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(climate_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_climate_information_when_filter_process_then_dont_call_query_builder(self):
        next(climate_filter.process(self.dissected_sentence_not_containing_importation_information, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_with_climate_information_when_extracting_then_returns_climate_information(self):
        climate_info = climate_filter.extract_climate(next(self.dissected_sentence))
        self.assertEqual(climate_info, CLIMATE_INFORMATION)
