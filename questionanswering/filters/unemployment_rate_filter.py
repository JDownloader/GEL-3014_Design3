from questionanswering import bidictionnary
import re
def process(question, query_builder):
    mapped_question = next(question)
    if ('unemployment' in mapped_question) & ('rate' in mapped_question):
        unemployment_rate = extract_unemployment_rate(mapped_question)
        for rate in unemployment_rate:
            if re.match('^[^.]*$', rate):
                query_builder.with_category_data('unemployment rate', ' '.join(unemployment_rate) + '.*')
            else:
                query_builder.with_category_data('unemployment rate', ' '.join(unemployment_rate))
    yield mapped_question

def extract_unemployment_rate(mappedSentence):
    reverse_dict = bidictionnary.Bidict(mappedSentence)
    return reverse_dict.keys_with_values(['CD'])
