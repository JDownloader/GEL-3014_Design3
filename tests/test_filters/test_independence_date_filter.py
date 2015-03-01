from unittest import TestCase

import mock
from questionanswering import question_processor
from questionanswering.filters import independence_date_filter
from questionanswering.query_builder import QueryBuilder

SENTENCE_CONTAINING_INDEPENDENCE_DATE_1 = "My independence was declared in August 1971."
SENTENCE_CONTAINING_INDEPENDENCE_DATE_2 = "In 1923, we proclaimed our independence."
SENTENCE_CONTAINING_INDEPENDENCE_DATE_3 = "What country has declared its independence on 22 May 1990?"
SENTENCE_CONTAINING_INDEPENDENCE_DATE_4 = "22 September 1960 is the date of independence of this country."

INDEPENDENCE_DATE_1 = ['1971', 'August']
INDEPENDENCE_DATE_2 = ['1923']
INDEPENDENCE_DATE_3 = ['22', '1990', 'May']
INDEPENDENCE_DATE_4 = ['22', '1960', 'September']

SENTENCE_NOT_CONTAINING_INDEPENDENCE_DATE = 'My telephone lines in use are 1.217 million.'

class TestIndependenceDateFilter(TestCase):

    def setUp(self):
        self.query_builder = QueryBuilder().with_category_data = mock.MagicMock()
        self.dissected_sentence_1 = question_processor.dissect_sentence(SENTENCE_CONTAINING_INDEPENDENCE_DATE_1, self.query_builder)
        self.dissected_sentence_2 = question_processor.dissect_sentence(SENTENCE_CONTAINING_INDEPENDENCE_DATE_2, self.query_builder)
        self.dissected_sentence_3 = question_processor.dissect_sentence(SENTENCE_CONTAINING_INDEPENDENCE_DATE_3, self.query_builder)
        self.dissected_sentence_4 = question_processor.dissect_sentence(SENTENCE_CONTAINING_INDEPENDENCE_DATE_4, self.query_builder)
        self.dissected_sentence_not_containing_independence_date = question_processor.dissect_sentence(SENTENCE_NOT_CONTAINING_INDEPENDENCE_DATE, self.query_builder)

    def test_given_dissected_sentence_containing_independence_date_information_when_independence_date_filter_process_then_calls_query_builder(self):
        self.assertTrue(next(independence_date_filter.process(self.dissected_sentence_1, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(independence_date_filter.process(self.dissected_sentence_2, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(independence_date_filter.process(self.dissected_sentence_3, self.query_builder)), self.query_builder.with_category_data.called)
        self.assertTrue(next(independence_date_filter.process(self.dissected_sentence_4, self.query_builder)), self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_not_containing_independence_date_information_when_independence_date_filter_process_then_dont_call_query_builder(self):
        next(independence_date_filter.process(self.dissected_sentence_not_containing_independence_date, self.query_builder))
        self.assertFalse(self.query_builder.with_category_data.called)

    def test_given_dissected_sentence_containing_independence_date_information_when_extracting_independence_date_then_returns_independence_date(self):
        independence_date_1 = question_processor.independence_date_filter.extract_independence_date_parts(next(self.dissected_sentence_1))
        independence_date_2 = question_processor.independence_date_filter.extract_independence_date_parts(next(self.dissected_sentence_2))
        independence_date_3 = question_processor.independence_date_filter.extract_independence_date_parts(next(self.dissected_sentence_3))
        independence_date_4 = question_processor.independence_date_filter.extract_independence_date_parts(next(self.dissected_sentence_4))

        self.assertEqual(independence_date_1, INDEPENDENCE_DATE_1)
        self.assertEqual(independence_date_2, INDEPENDENCE_DATE_2)
        self.assertEqual(independence_date_3, INDEPENDENCE_DATE_3)
        self.assertEqual(independence_date_4, INDEPENDENCE_DATE_4)