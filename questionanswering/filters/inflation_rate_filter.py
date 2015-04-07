from questionanswering import bidictionnary
from numpy import arange

def process(question, query_builder):
    mapped_question = next(question)
    if ('inflation' in mapped_question) and ('rate' in mapped_question):
        inflation_rate = extract_inflation_rate(mapped_question)
        if ('between' in mapped_question):
            numbers_in_range = process_between_inflation_rate(inflation_rate)
            query_builder.with_category_data('inflation rate', ' '.join(numbers_in_range))
        else :
            query_builder.with_category_data('inflation rate', ' '.join(inflation_rate))
    yield mapped_question

def extract_inflation_rate(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    return reverse_dict.keys_with_values(['CD'])

def process_between_inflation_rate(unemployment_rates):
    rates = arange(float(unemployment_rates[0]), float(unemployment_rates[1]),0.01)
    converted_rates = [str(item) for item in rates]
    return set(converted_rates).difference(unemployment_rates)
