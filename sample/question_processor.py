__author__ = 'Tea'

import nltk.corpus # 'maxent_treebank_pos_tagger', 'punkt' are attually used
from query_builder import QueryBuilder
from bidictionnary import Bidict
import elastic_search_client
import json

class QuestionProcessor :

    def start(self, question):
        query_builder = QueryBuilder()
        pipeline_steps = [dissect_sentence, capital_filter, fetch_answer]
        pipeline = combine_pipeline(question, query_builder, pipeline_steps)
        consume(pipeline)

def fetch_answer(question, query_builder):
    next(question)
    query = query_builder.build()

    client = elastic_search_client.ElasticSearchClient()
    response = client.post_request(query)
    if response != None :
        d = dict(json.loads(response)['hits']['hits'][0])
        print "response : " + d['_source']['country']
    yield

def independence_date_filter(question):
    mapped_question = next(question)
    yield mapped_question

def capital_filter(question, query_builder):
    mapped_question = next(question)
    if 'capital' in mapped_question:
        capital_name = process_capital_name(mapped_question)
        query_builder.withCapital(capital_name)
    yield mapped_question

def process_capital_name(mappedSentence):
    reverse_dict = Bidict(mappedSentence)

    if ("starts" in mappedSentence) & ("with" in mappedSentence) & ("ends" in mappedSentence):
        return reverse_dict.key_with_value('NNP') + reverse_dict.key_with_value('NNS')

    elif ("starts" in mappedSentence) & ("with" in mappedSentence):
        return reverse_dict.key_with_value('NNP') + "*"
    else:
        return reverse_dict.key_with_value('NNP')

def dissect_sentence(question, query_builder):
    tokenized_question = nltk.word_tokenize(question)
    tokenized_and_tagged_question = nltk.pos_tag(tokenized_question)
    yield dict(tokenized_and_tagged_question)

def combine_pipeline(source, query_builder, pipeline):
    return reduce(lambda x, y: y(x, query_builder) , pipeline, source)

def consume(iter):
    for _ in iter:
        pass

