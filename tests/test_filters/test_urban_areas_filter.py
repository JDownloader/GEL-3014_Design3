from unittest import TestCase
from questionanswering.filters import urban_areas_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_URBAN_AREAS_1 = "The major urban areas of this country are Santiago, Valparaiso and Concepcion. "
SENTENCE_CONTAINING_URBAN_AREAS_2 = "What country has major urban areas of 5.068 million and 1.098 million?"

URBAN_AREAS_1 = ['Valparaiso', 'Santiago', 'Concepcion']
URBAN_AREAS_2 = ['5.068', 'million', '1.098']

SENTENCE_NOT_CONTAINING_URBAN_AREAS = "What country has a latitude of 41.00 S?"


class TestUrbanAreaFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_URBAN_AREAS_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_URBAN_AREAS_2, self.query_builder)
        self.dissected_sentence_not_containing_urban_areas = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_URBAN_AREAS, self.query_builder)

    def test_given_dissected_sentence_containing_urban_areas_when_urban_areas_process_then_calls_query_builder(self):
        self.assertTrue(next(urban_areas_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(urban_areas_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_urban_areas_when_urban_areas_filter_process_then_dont_call_query_builder(self):
        next(urban_areas_filter.process(self.dissected_sentence_not_containing_urban_areas, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_urban_areas_when_extracting_urban_areas_then_returns_urban_areas(self):
        urban_areas_1 = question_processor.urban_areas_filter.extract_urban_areas(next(self.dissected_sentence_1))
        urban_areas_2 = question_processor.urban_areas_filter.extract_urban_areas(next(self.dissected_sentence_2))
        self.assertEqual(urban_areas_1, URBAN_AREAS_1)
        self.assertEqual(urban_areas_2, URBAN_AREAS_2)