from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import national_anthem_filter
from questionanswering.query_builder import QueryBuilder

SENTENCE_CONTAINING_NATIONAL_ANTHEM = "The title of my national anthem is Advance Australia Fair."

NATIONAL_ANTHEM = ['Advance', 'Australia', 'Fair']

SENTENCE_NOT_CONTAINING_NATIONAL_ANTHEM = 'My national symbol is the elephant.'

class TestNationalAnthemFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_NATIONAL_ANTHEM, self.query_builder)
        self.dissected_sentence_not_containing_national_anthem = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_NATIONAL_ANTHEM, self.query_builder)

    def test_given_dissected_sentence_containing_national_anthem_information_when_national_anthem_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(national_anthem_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_national_anthem_information_when_national_anthem_filter_process_then_dont_call_query_builder(self):
        next(national_anthem_filter.process(self.dissected_sentence_not_containing_national_anthem, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_national_anthem_information_when_extracting_national_anthem_name_then_returns_national_anthem(self):
        national_anthem = question_processor.national_anthem_filter.extract_national_anthem(next(self.dissected_sentence))
        self.assertEqual(national_anthem, NATIONAL_ANTHEM)
