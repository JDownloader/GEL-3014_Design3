from unittest import TestCase
from questionanswering.filters import telephone_lines_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_RELIGION =  "My telephone lines in use are 1.217 million."

TELEPHONES_LINES = '1.217 million'

SENTENCE_NOT_CONTAINING_TELEPHONES_LINES = "What country has a latitude of 41.00 S?"


class TestTelephoneLinesFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_RELIGION, self.query_builder)
        self.dissected_sentence_not_containing_telephone_lines = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_TELEPHONES_LINES, self.query_builder)

    def test_given_dissected_sentence_containing_telephone_lines_information_when_telephone_lines_process_then_calls_query_builder(self):
        self.assertTrue(next(telephone_lines_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_telephone_lines_information_when_telephone_lines_filter_process_then_dont_call_query_builder(self):
        next(telephone_lines_filter.process(self.dissected_sentence_not_containing_telephone_lines, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_containing_telephone_lines_information_when_extracting_telephone_lines_then_returns_telephone_lines(self):
        telephone_lines = question_processor.telephone_lines_filter.extract_total(next(self.dissected_sentence))

        self.assertEqual(telephone_lines, TELEPHONES_LINES)