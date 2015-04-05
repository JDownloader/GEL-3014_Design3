from unittest import TestCase
from questionanswering.filters import language_filter
from questionanswering.query_builder import QueryBuilder
from questionanswering import question_processor
import mock

SENTENCE_CONTAINING_LANGUAGE_INFORMATION =  "My languages include german, french and romansch."

LANGUAGES = ['german', 'french', 'romansch']

SENTENCE_NOT_CONTAINING_LANGUAGE_INFORMATION = "What country has religions including 51.3% of protestant and 0.7% of buddhist?"

class TestLanguageFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence = question_processor.dissect_sentence(SENTENCE_CONTAINING_LANGUAGE_INFORMATION, self.query_builder)
        self.dissected_sentence_not_containing_languages_information= question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_LANGUAGE_INFORMATION, self.query_builder)

    def test_given_dissected_sentence_containing_language_information_when_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(language_filter.process(self.dissected_sentence, self.query_builder)), self.query_builder.with_category_data.called)


    def test_given_dissected_sentence_not_containing_language_information_when_filter_process_then_dont_call_query_builder(self):
        next(language_filter.process(self.dissected_sentence_not_containing_languages_information, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_with_languages_information_when_extracting_then_returns_languages(self):
        languages_info = question_processor.language_filter.extract_languages(next(self.dissected_sentence))
        self.assertEqual(languages_info, LANGUAGES)

