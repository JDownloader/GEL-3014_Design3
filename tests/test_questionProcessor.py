from unittest import TestCase
from mock import Mock, patch
import types
from questionanswering import question_processor, query_builder

DUMMY_SENTENCE = "This is a sentence"

class TestQuestionProcessor(TestCase):

    def setUp(self):
        self.dummy_pipeline_steps = [first_dummy_method, second_dummy_method]
        self.query_builder_mock = Mock(spec=query_builder.QueryBuilder)
        self.question_processor = question_processor.QuestionProcessor()

    def test_combine_pipeline_returns_method_generators(self):
        dummy_pipeline = question_processor.combine_pipeline(DUMMY_SENTENCE, self.query_builder_mock, self.dummy_pipeline_steps)
        self.assertTrue(dummy_pipeline, (isinstance(method, types.GeneratorType) for method in dummy_pipeline))

    def test_dissect_sentence_tags_correctly_sentence(self):
        dissected_sentence = next(question_processor.dissect_sentence(DUMMY_SENTENCE, self.query_builder_mock))
        self.assertTrue(dissected_sentence, type({}))

#Test purpose only
def first_dummy_method(dummy_question, dummy_query_builder):
        yield
def second_dummy_method(dummy_question, dummy_query_builder):
        yield