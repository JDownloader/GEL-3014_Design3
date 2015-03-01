from unittest import TestCase
from questionanswering.filters import religion_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_RELIGION = "What country has religions including hindu, muslim, Christian, and sikh?"

RELIGION = ['hindu', 'muslim', 'Christian', 'sikh']

SENTENCE_NOT_CONTAINING_RELIGION = "What country has a latitude of 41.00 S?"

class TestReligionFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_RELIGION, self.query_builder)
        self.dissected_sentence_not_containing_religion = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_RELIGION, self.query_builder)

    def test_given_dissected_sentence_containing_religion_information_when_religion_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(religion_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_religion_information_when_religion_filter_process_then_dont_call_query_builder(self):
        next(religion_filter.process(self.dissected_sentence_not_containing_religion, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_containing_religion_information_when_extracting_religion_then_returns_religion(self):
        religion =  question_processor.religion_filter.extract_religions(next(self.dissected_sentence))

        self.assertEqual(religion, RELIGION)
