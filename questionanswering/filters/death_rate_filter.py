from questionanswering import bidictionnary
from numpy import arange, delete

def process(question, query_builder):
    mapped_question = next(question)
    if ('death' in mapped_question) and ('rate' in mapped_question):
        inflation_rate = extract_death_rate(mapped_question)
        if ('between' in mapped_question) or (('less' in mapped_question) and ('greater' in mapped_question) and ('than' in mapped_question)):
            numbers_in_range = process_between_rate(inflation_rate)
            query_builder.with_nested_query('death rate', ' '.join(numbers_in_range))
        else :
            query_builder.with_nested_query('death rate', ' '.join(inflation_rate + '.*'))
    yield mapped_question

def extract_death_rate(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    return reverse_dict.keys_with_values(['CD'])

def process_between_rate(death_rates):
    float_death_rates = [float(item) for item in death_rates]
    rates = arange(float(death_rates[0]), float(death_rates[1]), 0.01)
    for index, rate in enumerate(rates):
        if float(rate) in float_death_rates:
            rates = delete(rates, index)
    converted_rates = [str(item) for item in rates]
    return set(converted_rates).difference(death_rates)
