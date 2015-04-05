from unittest import TestCase
from questionanswering.filters import religion_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_RELIGION_1 = "What country has religions including hindu, muslim, Christian, and sikh?"
SENTENCE_CONTAINING_RELIGION_2 = "What country has religions including 51.3% of protestant and 0.7% of buddhist?"

RELIGION_INFORMATIONS_1 = ['hindu', 'muslim', 'Christian', 'sikh']
RELIGION_INFORMATIONS_2 = ['%', '51.3', 'protestant', 'buddhist', '0.7']

SENTENCE_NOT_CONTAINING_RELIGION = "What country has a latitude of 41.00 S?"

class TestReligionFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_RELIGION_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_RELIGION_2, self.query_builder)
        self.dissected_sentence_not_containing_religion = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_RELIGION, self.query_builder)

    def test_given_dissected_sentence_containing_religion_information_when_religion_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(religion_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(religion_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_religion_information_when_religion_filter_process_then_dont_call_query_builder(self):
        next(religion_filter.process(self.dissected_sentence_not_containing_religion, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_containing_religion_names_when_extracting_religion_then_returns_religions(self):
        religions =  question_processor.religion_filter.extract_religions(next(self.dissected_sentence_1))
        self.assertEqual(religions, RELIGION_INFORMATIONS_1)

    def test_given_dissected_sentence_containing_religion_names_and_rates_when_extracting_religion_then_returns_religions_with_rates(self):
        religions_with_rates =  question_processor.religion_filter.extract_religions_names_and_percentage(next(self.dissected_sentence_2))
        self.assertEqual(religions_with_rates, RELIGION_INFORMATIONS_2)