import json
from collections import OrderedDict
import nltk.corpus # 'maxent_treebank_pos_tagger', 'punkt' are attually used

import elastic_search_client
from query_builder import QueryBuilder
from filters import capital_filter, independence_date_filter, country_code_filter, national_symbol_filter, \
    urban_areas_filter, religion_filter, geographic_coordinates_filter, national_anthem_filter, \
    unemployment_rate_filter, population_growth_rate_filter, total_area_filter, population_filter,\
    telephone_lines_filter, language_filter, public_debt_filter, illicit_drugs_filter, industires_filter, \
    importation_filter, inflation_rate_filter, electricity_production_filter
class QuestionProcessor :
    def __init__(self):
        self.answer = ""

    def start(self, question):
        query_builder = QueryBuilder()
        pipeline_steps = [dissect_sentence, capital_filter.process, independence_date_filter.process,
                          country_code_filter.process, national_symbol_filter.process, urban_areas_filter.process,
                          religion_filter.process, geographic_coordinates_filter.process, national_anthem_filter.process,
                          unemployment_rate_filter.process, population_growth_rate_filter.process, total_area_filter.process,
                          population_filter.process, telephone_lines_filter.process, language_filter.process,
                          public_debt_filter.process, illicit_drugs_filter.process,
                          importation_filter.process, inflation_rate_filter.process, electricity_production_filter.process,
                          self.fetch_answer]
        pipeline = combine_pipeline(question, query_builder, pipeline_steps)
        consume(pipeline)

    def fetch_answer(self, question, query_builder):
        next(question)
        query = query_builder.build()
        print(query)
        client = elastic_search_client.ElasticSearchClient()
        response = client.post_request(query)

        try:
            self.answer = dict(json.loads(response)['hits']['hits'][0])['_source']['country']
        except IndexError:
            print "Woops, no answer to your question :("
        yield

def combine_pipeline(source, query_builder, pipeline):
    return reduce(lambda x, y: y(x, query_builder) , pipeline, source)

def consume(iter):
    for _ in iter:
        pass

def dissect_sentence(question, query_builder):
    # first use only to download nltk dictionnaries
    # nltk.download('punkls
    # nltk.download('maxent_treebank_pos_tagger')
    tokenized_question = nltk.word_tokenize(question)
    tokenized_and_tagged_question = nltk.pos_tag(tokenized_question)
    yield OrderedDict(tokenized_and_tagged_question)

