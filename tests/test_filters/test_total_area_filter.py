from unittest import TestCase
from questionanswering.filters import total_area_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_AREA = "What country has a total area of 390757 sq km?"

AREA = '390,757'

SENTENCE_NOT_CONTAINING_AREA = "What country has a latitude of 41.00 S?"


class TestTotalAreaFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_AREA, self.query_builder)
        self.dissected_sentence_not_containing_area= question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_AREA, self.query_builder)

    def test_given_dissected_sentence_containing_area_information_when_area_process_then_calls_query_builder(self):
        self.assertTrue(next(total_area_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_area_information_when_area_filter_process_then_dont_call_query_builder(self):
        next(total_area_filter.process(self.dissected_sentence_not_containing_area, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_containing_area_information_when_extracting_area_then_returns_area(self):
        total_area = question_processor.total_area_filter.extract_total_area(next(self.dissected_sentence))

        self.assertEqual(total_area, AREA)