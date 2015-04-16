from questionanswering import bidictionnary
from numpy import arange, delete

def process(question, query_builder):
    mapped_question = next(question)
    if ('birth' in mapped_question) and ('rate' in mapped_question):
        birth_rate = extract_birth_rate(mapped_question)
        if ('between' in mapped_question) or (('less' in mapped_question) and ('greater' in mapped_question) and ('than' in mapped_question)):
            numbers_in_range = process_between_rate(birth_rate)
            query_builder.with_nested_query('birth rate', ' '.join(numbers_in_range))
        else :
            adjusted_rates = []
            for rate in birth_rate:
                if (rate == '1000') | ('.' in rate):
                    adjusted_rates.append(rate)
                else:
                    adjusted_rates.append(rate + '.*')
            # adjusted_rates = [rate + '.*' for rate in birth_rate]
            query_builder.with_nested_query('birth rate', ' '.join(adjusted_rates))
    yield mapped_question

def extract_birth_rate(mapped_question):
    reverse_dict = bidictionnary.Bidict(mapped_question)
    return reverse_dict.keys_with_values(['CD'])

def process_between_rate(birth_rates):
    float_birth_rates = [float(item) for item in birth_rates]
    rates = arange(float(birth_rates[0]), float(birth_rates[1]), 0.01)
    for index, rate in enumerate(rates):
        if float(rate) in float_birth_rates:
            rates = delete(rates, index)
    converted_rates = [str(item) for item in rates]
    return set(converted_rates).difference(birth_rates)
