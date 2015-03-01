from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import geographic_coordinates_filter
from questionanswering.query_builder import QueryBuilder

SENTENCE_CONTAINING_GEOGRAPHIC_COORDINATES_1 = 'My latitude is 16 00 S and my longitude is 167 00 E'
SENTENCE_CONTAINING_GEOGRAPHIC_COORDINATES_2 = 'What country has a latitude of 41.00 S?'

GEOGRAPHIC_COORDINATES_1 = ['00', '16', 'S', '167', 'E']
GEOGRAPHIC_COORDINATES_2 = ['41 00', 'S']

SENTENCE_NOT_CONTAINING_GEOGRAPHIC_COORDINATES = 'My population growth rate is between 1.44% and 1.47%'

class TestGeographicCoordinatesFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_GEOGRAPHIC_COORDINATES_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_GEOGRAPHIC_COORDINATES_2, self.query_builder)
        self.dissected_sentence_not_containing_geographic_coordinates = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_GEOGRAPHIC_COORDINATES, self.query_builder)

    def test_given_dissected_sentence_containing_geographic_coordinates_information_when_geographic_coordinates_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(geographic_coordinates_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(geographic_coordinates_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_geographic_coordinates_information_when_geographic_coordinates_process_then_dont_call_query_builder(self):
        next(geographic_coordinates_filter.process(self.dissected_sentence_not_containing_geographic_coordinates, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_geographic_coordinates_information_when_extracting_geographic_coordinates_then_returns_geographic_coordinates(self):
        geographic_coordinates_1 = question_processor.geographic_coordinates_filter.extract_geographic_coordinates(next(self.dissected_sentence_1))
        geographic_coordinates_2 = question_processor.geographic_coordinates_filter.extract_geographic_coordinates(next(self.dissected_sentence_2))

        self.assertEqual(geographic_coordinates_1, GEOGRAPHIC_COORDINATES_1)
        self.assertEqual(geographic_coordinates_2, GEOGRAPHIC_COORDINATES_2)