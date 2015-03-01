from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import country_code_filter
from questionanswering.query_builder import QueryBuilder


SENTENCE_CONTAINING_COUNTRY_CODE_1 = 'What country has .dz as its internet country code?'
SENTENCE_CONTAINING_COUNTRY_CODE_2 = 'My internet country code is .br.'

COUNTRY_CODE_1 = '.dz'
COUNTRY_CODE_2 = '.br'

SENTENCE_NOT_CONTAINING_COUNTRY_CODE = 'My telephone lines in use are 1.217 million.'

class TestCountryCodeFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_COUNTRY_CODE_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_COUNTRY_CODE_2, self.query_builder)
        self.dissected_sentence_not_containing_country_code = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_COUNTRY_CODE, self.query_builder)

    def test_given_dissected_sentence_containing_country_code_information_when_country_code_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(country_code_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(country_code_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_country_code_information_when_country_code_filter_process_then_dont_call_query_builder(self):
        next(country_code_filter.process(self.dissected_sentence_not_containing_country_code, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_country_code_information_when_extracting_country_code_then_returns_country_code(self):
        country_code_1 = question_processor.country_code_filter.extract_country_code(next(self.dissected_sentence_1))
        country_code_2 = question_processor.country_code_filter.extract_country_code(next(self.dissected_sentence_2))

        self.assertEqual(country_code_1, COUNTRY_CODE_1)
        self.assertEqual(country_code_2, COUNTRY_CODE_2)
